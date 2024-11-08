# bedtime.ai

**bedtime.ai** is a personalized bedtime story system that uses a multi-model approach, combining voice cloning, natural language processing, and computer vision to create immersive bedtime stories. This project leverages state-of-the-art AI advancements to enhance the bedtime experience, allowing stories to be narrated in a parent's voice and tailored to each child’s interests or even their drawings. This fosters a stronger emotional connection and strengthens family bonds through personalized storytelling.

[Drawing Canvas] --> [Drawing Recognition] --> [Story Generation with Fine-Tuned LLM] --> [Personalized Narration (Cloned/Familar Voice)]

## Key Features
- **Personalized Story Generation:** A Fine-Tuned LLM (phi-3) is used to narrate bedtime stories based on a child’s interests, preferences, and drawings. This context-aware model dynamically adapts the story based on the child’s input and interaction.
  
- **Voice Cloning:** The system uses advanced voice synthesis techniques to replicate a parent’s voice, narrating the story in a familiar, comforting tone.
  
- **Interactive Storytelling:** Children can draw on the canvas, which the system then incorporates into the stories, making the experience more engaging and uniquely personal.

## Architecture
The bedtime.ai system utilizes several machine learning models in a multi-model pipeline to deliver a complete and immersive experience:

## Architecture

1. **Story Generation Model**  
   - A fine-tuned language model generates bedtime stories based on the child’s inputs. The model adapts content dynamically, ensuring engaging and relevant stories every night.

2. **Voice Cloning Model**  
   - Advanced voice cloning techniques are used to narrate the generated story in a parent’s voice. This is achieved using a speaker encoder-decoder architecture that synthesizes high-quality, natural-sounding narration.

3. **Computer Vision Model**  
   - An EfficientNet model fine-tuned on children’s drawings detects and interprets uploaded drawings or images. These inputs are then integrated into the story generation model, automatically tailoring the story’s content to include elements from the visual input.

4. **Backend & API**  
   - A FastAPI backend coordinates user requests, model execution, and data flow. This backend manages user interactions, story generation, and API calls to the various models for real-time, personalized responses.

5. **User Interface (UI)**  
   - The user interface is built with React and Vite, providing a seamless and responsive experience. This front-end setup enables easy interaction for uploading preferences and drawings, as well as accessing generated stories.

6. **Containerization**  
   - Docker is used to containerize the services, ensuring consistent and isolated environments for each model and the backend. This simplifies deployment and enhances scalability across different environments.



![image](https://github.com/user-attachments/assets/309612e3-593d-4ff1-8bf6-26f5a991826a)


