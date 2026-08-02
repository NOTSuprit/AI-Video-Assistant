<div align="center">

# 🎬 AI Video Assistant

**Turn any YouTube video or local recording into a searchable, summarized, chat-ready transcript.**

Transcribe → Summarize → Chat, all running on local, open-source models.

</div>

---

## Overview

AI Video Assistant is a Streamlit app that takes a YouTube URL (or a local audio/video file), and runs it through a full meeting-intelligence pipeline:

1. **Audio acquisition** — downloads audio from YouTube (`yt-dlp`) or accepts a local file
2. **Transcription** — transcribes speech locally using OpenAI's Whisper, with Hindi → English translation support
3. **Title generation** — auto-generates a concise session title from the transcript
4. **Summarization** — produces a structured summary (key risks/challenges, root causes, action items, key decisions, open questions) via LangChain + Mistral
5. **RAG chat** — indexes the transcript into a vector store (ChromaDB) so you can ask follow-up questions and get grounded answers with supporting quotes

No transcript ever needs to leave your machine to get to step 3 — the heavy lifting (speech-to-text) runs locally.

---

## ✨ Features

- 📥 **Flexible input** — paste a YouTube URL or point to a local audio/video file
- 🗣️ **Local transcription** — Whisper-based, with automatic Hindi→English translation
- 🏷️ **Auto-generated titles** — no more "Untitled Meeting"
- 📋 **Structured summaries** — key risks, root causes, action items, key decisions, and open questions extracted automatically
- 💬 **Chat with your transcript** — RAG-powered Q&A grounded in the actual transcript, with quoted evidence
- 🔄 **Live pipeline status** — see each stage (audio processing → transcription → title generation → summarization → extraction) complete in real time
- 🛡️ **Resilient YouTube extraction** — works around Cloudflare/JS-challenge and DRM-restricted player clients using a runtime-installed Deno JS interpreter and cookie-based auth

---

## 🖼️ Screenshots

<table>
<tr>
<td width="50%">

**Structured Summary**

Session title, key challenges, and root-cause breakdown generated automatically from the transcript.

![Summary view]([./assets/summary-view.png](https://github.com/NOTSuprit/AI-Video-Assistant/blob/main/utils/Screenshot%202026-08-03%20at%2003.17.45.png))

</td>
<td width="50%">

**Action Items, Key Decisions & Chat**

Extracted action items and open questions, plus the chat interface for asking follow-up questions.

![Action items and chat]([./assets/action-items-chat.png](https://github.com/NOTSuprit/AI-Video-Assistant/blob/main/utils/Screenshot%202026-08-03%20at%2003.18.00.png))

</td>
</tr>
</table>

**Chat with your transcript, grounded in the source material:**

![RAG chat with quoted evidence]([./assets/rag-chat.png](https://github.com/NOTSuprit/AI-Video-Assistant/blob/main/utils/Screenshot%202026-08-03%20at%2003.19.07.png))

---

## 🏗️ Architecture

```
AI-Video-Assistant/
├── app.py                  # Streamlit entrypoint & UI
├── main.py                 # Pipeline orchestration
├── deno_setup.py           # Runtime Deno installer (for yt-dlp JS-challenge solving)
├── core/
│   ├── extractor.py         # YouTube URL detection / metadata extraction
│   ├── transcriber.py       # Whisper-based transcription
│   ├── summarizer.py        # LangChain + Mistral summarization
│   ├── rag_engine.py        # RAG chat over the transcript
│   └── vector_store.py      # ChromaDB vector store setup
├── utils/
│   └── audio_processor.py   # yt-dlp download + audio conversion (WAV)
├── packages.txt             # apt-level dependencies (ffmpeg)
└── requirements.txt         # Python dependencies
```

**Pipeline flow:**

```
YouTube URL / local file
        │
        ▼
 audio_processor.py  ──►  raw audio → WAV (via yt-dlp + FFmpeg)
        │
        ▼
   transcriber.py     ──►  Whisper transcription (+ Hindi→English if needed)
        │
        ▼
   summarizer.py       ──►  title, summary, action items, key decisions, open questions
        │
        ▼
   vector_store.py      ──►  transcript embedded into ChromaDB
        │
        ▼
   rag_engine.py          ──►  chat interface grounded in the transcript
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.12
- [FFmpeg](https://ffmpeg.org/) (installed automatically via `packages.txt` on Streamlit Cloud; install locally with your package manager, e.g. `brew install ffmpeg`)
- A [Mistral AI](https://mistral.ai/) API key (for summarization and RAG chat)

### Installation

```bash
git clone https://github.com/NOTSuprit/AI-Video-Assistant.git
cd AI-Video-Assistant

python3 -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

pip install -r requirements.txt
```

### Configuration

Create a `.env` file in the project root:

```env
MISTRAL_API_KEY=your_mistral_api_key_here
```

**YouTube downloads (optional but recommended):** to reduce YouTube bot-detection / DRM issues, export your browser's YouTube cookies to a `cookies.txt` file (Netscape format) in the project root. Both `.env` and `cookies.txt` are gitignored by default — never commit either.

### Run locally

```bash
streamlit run app.py
```

Then open `http://localhost:8501`, paste a YouTube URL or local file path, and hit **Analyse**.

---

## ☁️ Deployment Notes

This app is built to run on [Streamlit Community Cloud](https://streamlit.io/cloud), with a few environment-specific considerations baked in:

- **`packages.txt`** installs `ffmpeg` as an apt dependency.
- **`deno_setup.py`** downloads a portable Deno binary to `/tmp` at runtime, since Streamlit Cloud's container doesn't ship one and yt-dlp needs a JS runtime to solve YouTube's signature challenges.
- **YouTube cookies** should be provided via [Streamlit Secrets](https://docs.streamlit.io/develop/concepts/connections/secrets-management) as `COOKIES_TXT`, rather than committed to the repo, since cloud IPs are more aggressively bot-checked than residential ones.
- **`player_client`** is set to try `android`, `ios`, and `web` in order — YouTube periodically DRM-restricts specific clients (e.g. `tv`), so falling back across clients improves reliability.

YouTube's anti-bot measures (DRM-gated clients, SABR-only experiments, PO token requirements) change fairly often — if downloads start failing, `pip install -U yt-dlp` first, since the maintainers typically ship fixes quickly.

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| UI | [Streamlit](https://streamlit.io/) |
| Audio acquisition | [yt-dlp](https://github.com/yt-dlp/yt-dlp), FFmpeg, pydub |
| Transcription | [OpenAI Whisper](https://github.com/openai/whisper) (local), PyTorch |
| Translation | Hugging Face Transformers |
| Summarization | [LangChain](https://www.langchain.com/) + [Mistral AI](https://mistral.ai/) |
| RAG / vector store | ChromaDB, Sentence Transformers, LangChain Hugging Face embeddings |
| Export | fpdf2 |

---

## 🗺️ Roadmap

- [ ] Pluggable PO-token provider for more resilient YouTube auth on cloud deployments
- [ ] Support for additional source languages beyond Hindi→English
- [ ] Export summaries/transcripts as PDF/TXT from the UI
- [ ] Batch processing for multiple videos

---

## 📄 License

No license specified yet — add one (e.g. MIT) if you intend for others to use or contribute to this project.

---

<div align="center">

Built by [NOTSuprit](https://github.com/NOTSuprit)

</div>
