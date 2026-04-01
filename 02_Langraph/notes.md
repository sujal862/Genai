
# SEE MINI_CURSOR :  for tool calling -> agent (loop) : very important

# Langgraph
**LangGraph** ek framework hai jo AI workflows ko **graph (flowchart)** ki tarah organize karta hai. Isme **nodes = tasks (chhote kaam)** hote hain, jaise “code fetch karo”, “analyze karo”, “review generate karo”. 
**Edges = connections/flow** hote hain jo batate hain ki ek task ke baad kaunsa task chalega. **State = shared data/memory** hoti hai jo har step ke beech pass hoti hai (jaise diff, analysis, review). Iska main use hota hai **multi-step AI systems** banane me jahan simple linear flow kaafi nahi hota—yahan tu branching, looping, aur decision-based execution control kar sakta hai. Simple words me: 

“Each node processes and updates shared state, and the final output is derived from the accumulated state”
Each node can recieve the current state as input and output an update to the state

**LangGraph = structured system jo AI ko step-by-step intelligently kaam karne deta hai instead of random calls.**
