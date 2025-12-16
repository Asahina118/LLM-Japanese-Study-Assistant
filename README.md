# LLM-Japanese-Study-Assistant
runs local llms in Ollama and PyQt6 to analyze the grammar of japanese and categorize the input into corresponding JLPT level.

Implemented:
GUI in PyQt6
ollama server is managed in the app. You do not need to run the headless server in the terminal separately.
running llm on separate thread to prevent GUI from freezing.

TO DO:
pulling models directly in the app
supports screenshot text recognition (screenshot implemented)
RAG implementation on better JLPT level recognition
tracking frequency of grammar encountering
