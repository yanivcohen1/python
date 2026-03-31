import yt_dlp
import multiprocessing
import threading
import time
import sys

# --- Global variables for queue and process management ---
queue_lock = threading.Lock()
pending_queue = []
active_downloads = []
MAX_CONCURRENT = 3
download_counter = 1
app_running = True


def download_video_720p(task_id, url, output_path, shared_status, slot):
    """
    Performs the download and updates progress percentages in the shared dictionary
    """

    file_exists = [False]

    class YTDLLogger:
        def debug(self, msg):
            if "already been downloaded" in msg.lower() or "already exists" in msg.lower():
                file_exists[0] = True
                s = f"⚠️ File already exists, skipping. [ID: {task_id}]"
                shared_status[task_id] = s
                sys.stdout.write(f"\033[s\033[{slot}A\r\033[K{s}\033[u")
                sys.stdout.flush()
        def info(self, msg):
            if "already been downloaded" in msg.lower() or "already exists" in msg.lower():
                file_exists[0] = True
                s = f"⚠️ File already exists, skipping. [ID: {task_id}]"
                shared_status[task_id] = s
                sys.stdout.write(f"\033[s\033[{slot}A\r\033[K{s}\033[u")
                sys.stdout.flush()
        def warning(self, msg):
            pass
        def error(self, msg):
            pass

    # Inner function that hooks the status from yt-dlp in real time
    def progress_hook(d):
        import re
        if d["status"] == "downloading":
            # Retrieves the download percentage and cleans hidden characters
            percent = d.get("_percent_str", "0.0%").strip()
            speed = d.get("_speed_str", "N/A").strip()

            # Clean terminal color formatting (ANSI escape codes)
            clean_percent = re.sub(r'\x1b\[[0-9;]*m', '', percent).strip()

            # Create a visual progress bar
            try:
                # Build an accurate float, handling yt-dlp's estimated sizes like "~10.5%"
                num_match = re.search(r'([0-9]+(?:\.[0-9]+)?)', clean_percent)
                if num_match:
                    p_val = float(num_match.group(1))
                    bar_len = 20
                    filled = int((p_val / 100) * bar_len)
                    bar = '█' * filled + '░' * (bar_len - filled)
                    status_text = f"Downloading [ID: {task_id}]: [{bar}] {clean_percent} (Speed: {speed})"
                else:
                    status_text = f"Downloading [ID: {task_id}]: {clean_percent} (Speed: {speed})"
            except Exception:
                status_text = f"Downloading [ID: {task_id}]: {clean_percent} (Speed: {speed})"

            # Save status in shared memory
            shared_status[task_id] = status_text

            # Print live output above the input line without interrupting it
            # Uses `slot` to ensure concurrent downloads don't overwrite each other's lines
            # \033[s  - שומר את מיקום הסמן הנוכחי
            # \033[{i}A  - עולה אינדקס שורת למעלה
            # \r      - חוזר לתחילת השורה
            # \033[K  - מוחק את כל מה שיש בשורה (כדי שלא יישארו שאריות)
            # \033[u  - מחזיר את הסמן למיקום שנשמר
            sys.stdout.write(f"\033[s\033[{slot}A\r\033[K{status_text}\033[u")
            sys.stdout.flush()
        elif d["status"] == "finished":
            if file_exists[0]:
                return
            bar = '█' * 20
            status_text = f"Downloading [ID: {task_id}]: [{bar}] 100.0% - Finalizing..."
            shared_status[task_id] = status_text
            sys.stdout.write(f"\033[s\033[{slot}A\r\033[K{status_text}\033[u")
            sys.stdout.flush()

    ydl_opts = {
        "outtmpl": f"{output_path}/%(title)s.%(ext)s",
        "format": "bestvideo[height<=720][ext=mp4]+bestaudio[ext=m4a]/bestvideo[height<=720]+bestaudio/best[height<=720][ext=mp4]/best[height<=720]",
        "noplaylist": True,
        "merge_output_format": "mkv",
        "quiet": True,  # Silences yt-dlp printing to screen
        "no_warnings": True,
        "concurrent_fragment_downloads": 10,
        "ffmpeg_location": "D:\\Temp\\interview\\ffmpeg-master-latest-win64-gpl\\bin",
        "progress_hooks": [progress_hook],  # Hooks our tracking function
        "logger": YTDLLogger(),  # Hooks yt-dlp internal messages to catch existing files
        "writethumbnail": True,
        "postprocessors": [
            {"key": "FFmpegVideoRemuxer", "preferedformat": "mkv"},
            {"key": "FFmpegThumbnailsConvertor", "format": "jpg"},
            {"key": "EmbedThumbnail"}
        ],
        "fixup": "force", # Force yt-dlp to fix file structural issues
        "continuedl": False,
        # Use native downloader for the PROGRESS BAR
        # Fix HLS streaming corruption
        "hls_use_mpegts": True,
    }

    shared_status[task_id] = "Starting connection..."
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            
        # Do not override the status if it has already been set to "File already exists"
        if not file_exists[0]:
            bar = '█' * 20
            final_text = f"✅ Finished [ID: {task_id}]: [{bar}] 100.0% (thumbnail embedded in .mkv)"
            shared_status[task_id] = final_text
            sys.stdout.write(f"\033[s\033[{slot}A\r\033[K{final_text}\033[u")
            sys.stdout.flush()
    except Exception:
        error_text = f"❌ Error/Cancelled [ID: {task_id}]"
        shared_status[task_id] = error_text
        sys.stdout.write(f"\033[s\033[{slot}A\r\033[K{error_text}\033[u")
        sys.stdout.flush()


def queue_manager(shared_status):
    """Queue manager running in background"""
    global app_running
    while app_running:
        with queue_lock:
            # 1. Clean up finished processes
            for item in active_downloads[:]:
                if not item["process"].is_alive():
                    item["process"].join()
                    active_downloads.remove(item)

            # 2. Insert new downloads from the queue
            while len(active_downloads) < MAX_CONCURRENT and len(pending_queue) > 0:
                next_item = pending_queue.pop(0)

                # Find an available slot (1 to MAX_CONCURRENT) so progress bars don't overlap
                used_slots = [item["slot"] for item in active_downloads]
                slot = 1
                for i in range(1, MAX_CONCURRENT + 1):
                    if i not in used_slots:
                        slot = i
                        break

                # Create a new process, passing ID and shared memory
                p = multiprocessing.Process(
                    target=download_video_720p,
                    args=(
                        next_item["id"],
                        next_item["url"],
                        "C:\\Users\\yaniv\\Downloads\\videos",
                        shared_status,
                        slot,
                    ),
                    name=f"Worker-[ID:{next_item['id']}]",
                )
                p.start()

                active_downloads.append(
                    {"id": next_item["id"], "url": next_item["url"], "process": p, "slot": slot}
                )
        time.sleep(1)


if __name__ == "__main__":
    # Create a shared dictionary for all processes to read/write
    manager = multiprocessing.Manager()
    shared_status = manager.dict()

    print("--- Download Manager (up to 3 concurrent + progress tracking) ---")
    print("Type 'list' or 'status' to see live progress percentages.")
    print("Type 'remove <ID>' to cancel a download (even if it has started).")
    print("Type '(ctrl+c)' to FORCE STOP (killed) all active downloads immediately.\n")
    print("Type 'quit' to exit.\n")

    manager_thread = threading.Thread(
        target=queue_manager, args=(shared_status,), daemon=True
    )
    manager_thread.start()

    while True:
        try:
            # Pre-allocate lines above each new prompt so active downloads won't overwrite history
            print("\n" * MAX_CONCURRENT, end="")
            cmd = input("Enter link or command: ").strip()
            if not cmd:
                continue
            cmd_lower = cmd.lower()

            # --- Exit command ---
            if cmd_lower in ["quit", "q", "exit"]:
                print("\nExiting... clearing pending queue and waiting for active downloads to finish.")
                app_running = False
                with queue_lock:
                    pending_queue.clear()
                for item in active_downloads:
                    item["process"].join()
                break

            # --- Force kill ---
            elif cmd_lower == "killed":
                print("\nStopping everything immediately...")
                app_running = False
                with queue_lock:
                    pending_queue.clear()
                    for item in active_downloads:
                        if item["process"].is_alive():
                            item["process"].terminate()
                            item["process"].join()
                break

            # --- Show download status (progress bars) ---
            elif cmd_lower in ["list", "status"] or cmd_lower == "s":
                with queue_lock:
                    print("\n--- 📊 Download Status ---")
                    if not active_downloads and not pending_queue:
                        print("No active or pending downloads.")
                    else:
                        for item in active_downloads:
                            t_id = item["id"]
                            # Read real-time status from shared memory
                            current_status = shared_status.get(t_id, "Loading...")
                            print(f"  [ID: {t_id}] 🟢 {current_status}")

                        for item in pending_queue:
                            print(f"  [ID: {item['id']}] ⏳ Waiting in queue...")
                    print("------------------------\n")

            # --- Remove/cancel download ---
            elif cmd_lower.startswith("remove "):
                try:
                    id_to_remove = int(cmd_lower.split(" ")[1])
                    with queue_lock:
                        found = False
                        # 1. Try to remove from pending queue
                        pending_ids = [i["id"] for i in pending_queue]
                        if id_to_remove in pending_ids:
                            pending_queue = [
                                i for i in pending_queue if i["id"] != id_to_remove
                            ]
                            print(f"✅ [ID: {id_to_remove}] removed from pending queue.")
                            found = True

                        # 2. Check if the download is currently active
                        if not found:
                            for item in active_downloads:
                                if item["id"] == id_to_remove:
                                    if item["process"].is_alive():
                                        item[
                                            "process"
                                        ].terminate()  # Force kill the process
                                        item["process"].join()
                                    active_downloads.remove(item)
                                    shared_status[id_to_remove] = (
                                        "🛑 Cancelled by user"
                                    )
                                    print(
                                        f"🛑 [ID: {id_to_remove}] was downloading - cancelled and stopped!"
                                    )
                                    found = True
                                    break

                        if not found:
                            print(f"❌ No download found with ID {id_to_remove}.")
                except ValueError:
                    print(
                        "❌ Error: type 'remove' followed by a number (e.g., 'remove 5')."
                    )

            # --- Add new link ---
            else:
                with queue_lock:
                    pending_queue.append({"id": download_counter, "url": cmd})
                    shared_status[download_counter] = "Added to queue"
                    print(f"✅ Added to queue under [ID: {download_counter}]")
                    download_counter += 1

        except KeyboardInterrupt:
            print("\nEmergency stop triggered...")
            app_running = False
            for item in active_downloads:
                if item["process"].is_alive():
                    item["process"].terminate()
                    item["process"].join()
            break

    print("Goodbye!")
