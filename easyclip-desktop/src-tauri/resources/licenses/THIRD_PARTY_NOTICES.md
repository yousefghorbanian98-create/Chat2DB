# EasyClip Desktop third-party notices

The Windows installer is an aggregate that includes the following unmodified, separately executable/runtime components. Their license texts are shipped beside this notice in the installed application resources.

## FFmpeg 9.0.1 (Gyan essentials build)

- Binary: `ffmpeg.exe`, `ffprobe.exe`
- Project: https://ffmpeg.org/
- Windows build: https://github.com/GyanD/codexffmpeg/releases/tag/9.0.1
- Corresponding FFmpeg source: https://github.com/FFmpeg/FFmpeg/tree/n9.0.1
- Build artifact SHA-256: `fec81ae03971d9dd4be3ebe02e263bd2ec1d789483f931bdba5f5715e65da2e9`
- License: GNU General Public License v3.0 or later (`FFmpeg-GPL-3.0.txt`). The selected build includes GPL libraries such as libx264 and libass dependencies used by EasyClip.

## whisper.cpp 1.9.2

- Binary: `whisper-cli.exe` and its adjacent runtime libraries
- Project/source: https://github.com/ggml-org/whisper.cpp/tree/v1.9.2
- Build artifact SHA-256: `49dcc16de826f20bd53d44f947a1ae49dfa81f86cad67a64d80820cb192d674a`
- License: MIT (`whisper.cpp-MIT.txt`)

## OpenAI Whisper multilingual base model

- Model: `ggml-base.bin`, converted for whisper.cpp
- Model repository: https://huggingface.co/ggerganov/whisper.cpp
- Upstream project: https://github.com/openai/whisper
- Model SHA-256 / Git LFS object: `60ed5bc3dd14eea856493d334349b405782ddcaf0028d4b5df4088345fba2efe`
- License: MIT (`Whisper-model-MIT.txt`)

## Noto Sans Arabic

- Font: `NotoSansArabic.ttf`
- Source snapshot: https://github.com/google/fonts/tree/73fc2ff52147e34a74804b500cf89ca219eac55d/ofl/notosansarabic
- Font SHA-256: `63111b5b2e074dd48cc67692e0a2726d86ee94c1c37fe8598257b7b4e87e869e`
- License: SIL Open Font License 1.1 (`Noto-Sans-Arabic-OFL-1.1.txt`)

The complete corresponding sources remain available at the immutable links above. EasyClip invokes FFmpeg and whisper.cpp as separate programs and does not link their code into the EasyClip Rust executable.
