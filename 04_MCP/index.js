import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js"
import {z} from "zod"
import axios from "axios";
// Transport: Claude aur server ke beech communication
// Stdio = standard input/output (terminal ke through)
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";


const server = new McpServer({
    name: 'My Server', // Claude is naam se server ko identify karega
    version: '1.0.0',
    description: 'My Server',
});

// Tool Register Karo
// Arg 1: Tool ka naam — Claude isse call karega
// Arg 2: IMPORTANT: Description — Claude isi ko padhta hai decide karne ke liye : "kab ye tool use karna chahiye"
// Arg 3: Input schema (Zod): Claude ko batata hai — kya bhejno hai
// Arg 4: Handler (Async function): Actual tool logic
server.tool("add",
    "Adds two numbers together",
    {a: z.number(), b:z.number()},
    async({a, b}) => {
        const sum = a+b;
        // Return format FIXED hai — content array required hai : { content: [{ type, text }] }
        return { content: [{type: "text", text: String(sum)}]}
    }
)


server.tool(
  'weather',
  "Get weather of any city",
  { city: z.string().describe('Name of the city') },
  async function ({ city }) {
    const response = await axios.get(`https://wttr.in/${city}?format=%C+%t`, {
      responseType: 'json',
    });
    return { content: [{ type: 'text', text: JSON.stringify(response.data) }] };
  }
);

const transport = new StdioServerTransport();

// Server ko transport se connect karo
// Iske baad server requests sunna shuru kar deta hai
await server.connect(transport);