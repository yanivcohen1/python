import { initializeAgentExecutorWithOptions } from "langchain/agents";
import { ChatOpenAI } from "langchain/chat_models/openai";
import { SerpAPI } from "langchain/tools";        // כלי חיפוש אינטרנט (SerpAPI)
import { Calculator } from "langchain/tools/calculator";  // כלי מחשבון

// הגדרת מפתחות API (יש לספק מפתחות אמיתיים כאן)
process.env["OPENAI_API_KEY"] = "OPENAI_KEY_כאן";
process.env["SERPAPI_API_KEY"] = "SERPAPI_KEY_כאן";

// אתחול הכלים והמודל
const tools = [ new Calculator(), new SerpAPI() ];
const model = new ChatOpenAI({ modelName: "gpt-3.5-turbo", temperature: 0 });

// יצירת ה-Executor של הסוכן עם הכלים והמודל
const executor = await initializeAgentExecutorWithOptions(tools, model, {
  agentType: "openai-functions",
  verbose: true // נשתמש בפלט מפורט לצורך הדגמה
});

// הרצת השאילתה דרך הסוכן
const result = await executor.run(
  "מצא כמה אלבומים הוציא הזמר Nas מאז 2010, וכמה אלבומים הוציא Boldy James מאז 2010. מי הוציא יותר ומה ההפרש באחוזים?"
);

console.log(result);
