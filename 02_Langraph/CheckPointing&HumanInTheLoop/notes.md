### Role of `interrupt()`
- `interrupt()` **pauses** the graph.
- It sends some data/context to the client.
- This helps the human understand:
  - What is happening
  - What input is needed

### Human Decision Flow
- After interruption, a human reviews the situation.
- The human decides what to do next (approve, modify, or respond).

### Resuming Execution
- To continue, the client must use:
  ```python
  Command(resume=...)
  ```
- This sends the human's input back into the graph.
- The graph then:
  - Resumes execution
  - Restarts from the same node
  - Re-runs the logic with new input



# FLOW :
1. User Input
-User sends a message (e.g., “I need help logging in”).
-A thread_id is passed → used to track and store this conversation in MongoDB.

2. Chatbot Node Runs
-Graph starts and goes to chatbot node.
-LLM reads the message.
-If needed, it decides to call a tool (like human_assistance_tool).
-Behind the scenes, the Checkpointer silently saves the current state containing the LLM's new "Tool Call Request" to MongoDB.

3. Condition Check
-tools_condition checks:
-If tool is needed → go to tools node
-Else → end the flow

4. Tools Node + Pause
-Tool starts executing.
-interrupt() is hit → graph pauses immediately.
-interrupt() tells LangGraph: "STOP right here!" The graph immediately Halts. The Checkpointer performs a critical save to MongoDB, storing the exact paused state, and exits out of the app.main script completely.

5. Human Support
- The support agent runs app.support.py using the exact same thread_id from config
- Database Fetch: LangGraph connects to MongoDB via the checkpointer, looks up thread "1", and realizes: "Wait, this graph was paused in the middle of a tool execution!"
- Human reads paused state and issue and writes a response.

6. Resume Graph
-app.support issues a Command(resume={"data": ans}) to the graph.
-LangGraph wakes back up, injects the human's answer directly into the interrupt()
 line where it was frozen, and finishes the human_assistance_tool.
-Updated state is saved.

7. Final Response
-Flow goes back to chatbot node bec **graph_builder.add_edge("tools", "chatbot")**
-LLM combines:
-original request
-human response
-Sends final reply to user.
-Graph ends and state is saved.

In One Line:
User → LLM → Tool → Pause → Human → Resume → LLM → Final Answer
