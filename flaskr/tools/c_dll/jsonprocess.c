#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// Example C function that processes JSON
const char* process_json(const char* input_json) {
    const char* my_str = "my cmd_";

    // Calculate the size needed for the concatenated string
    size_t size = strlen(input_json) + strlen(my_str) + 1;

    // Allocate memory for the concatenated string
    char* output_json = (char*)malloc(size);

    if (output_json == NULL) {
        fprintf(stderr, "Memory allocation failed\n");
        return NULL;
    }

    // Concatenate the strings
    // Concatenate the parts into the new UTF-8 encoded string
    strcpy(output_json, my_str);
    strcat(output_json, input_json);

    // Print the concatenated string
    printf("c print: %s\n", output_json);

    // Free the allocated memory
    // free(utf8_str);

    return output_json;
}

// Example C function that processes JSON
const char* process_file(const char* input_str) {
    // Calculate the size of the original JSON string
    size_t size = strlen(input_str) + 1; // +1 for the null terminator

    // Allocate memory for the copy
    char* output_str = (char*)malloc(size);

    if (output_str == NULL) {
        fprintf(stderr, "Memory allocation failed\n");
        return NULL;
    }

    // Copy the original JSON string into the allocated memory
    strcpy(output_str, input_str);

    // Free the allocated memory
    // free(output_str);

    return output_str;
}
