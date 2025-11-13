import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any

app = FastAPI(title="AI Power - Hyper Generate API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class StoryboardFrame(BaseModel):
    t: float
    title: str
    description: str
    camera: str
    elements: List[str]


class AudioLayer(BaseModel):
    name: str
    type: str
    waveform: str
    notes: Optional[List[float]] = None
    base_freq: Optional[float] = None
    lfo_freq: Optional[float] = None
    reverb: Optional[float] = None
    volume: float = 0.5


class HyperGenerateRequest(BaseModel):
    prompt: str


class HyperGenerateResponse(BaseModel):
    prompt: str
    code_snippets: Dict[str, str]
    video: Dict[str, Any]
    audio: Dict[str, Any]
    image_svg: str
    text_response: str


@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI Backend!"}


@app.get("/api/hello")
def hello():
    return {"message": "Hello from the backend API!"}


@app.get("/test")
def test_database():
    """Test endpoint to check if database is available and accessible"""
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }

    try:
        from database import db

        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Configured"
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"

    except ImportError:
        response["database"] = "❌ Database module not found (run enable-database first)"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"

    import os
    response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"

    return response


def build_image_svg(prompt: str) -> str:
    # Generate a high-res SVG with a monolith and electric blue glow
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="2400" height="1350" viewBox="0 0 2400 1350">
      <defs>
        <radialGradient id="glow" cx="50%" cy="60%" r="60%">
          <stop offset="0%" stop-color="#6EE7F9" stop-opacity="0.9"/>
          <stop offset="40%" stop-color="#2563EB" stop-opacity="0.35"/>
          <stop offset="100%" stop-color="#0B1020" stop-opacity="0"/>
        </radialGradient>
        <linearGradient id="sky" x1="0" x2="0" y1="0" y2="1">
          <stop offset="0%" stop-color="#070914"/>
          <stop offset="100%" stop-color="#0B1020"/>
        </linearGradient>
        <filter id="blur">
          <feGaussianBlur in="SourceGraphic" stdDeviation="40"/>
        </filter>
      </defs>
      <rect width="100%" height="100%" fill="url(#sky)"/>
      <g opacity="0.25">
        {''.join([f'<circle cx="{i*220}" cy="{(i*97)%1350}" r="{80+(i%5)*18}" fill="#6B21A8" opacity="0.25"/>' for i in range(1,20)])}
      </g>
      <ellipse cx="1200" cy="980" rx="800" ry="220" fill="#0B1020" opacity="0.9"/>
      <ellipse cx="1200" cy="980" rx="820" ry="240" fill="#1E293B" opacity="0.35" filter="url(#blur)"/>
      <rect x="1100" y="300" width="200" height="700" rx="8" fill="#0F172A" stroke="#1E293B" stroke-width="3"/>
      <rect x="1110" y="310" width="180" height="680" rx="6" fill="#111827"/>
      <rect x="1120" y="320" width="160" height="660" rx="4" fill="#0B1325"/>
      <rect x="1128" y="330" width="144" height="640" rx="3" fill="#0A0F1D"/>
      <ellipse cx="1200" cy="980" rx="520" ry="140" fill="url(#glow)"/>
      <circle cx="1200" cy="620" r="420" fill="url(#glow)"/>
      <text x="1200" y="1240" text-anchor="middle" font-family="Inter, system-ui" font-size="28" fill="#94A3B8" opacity="0.9">{prompt}</text>
    </svg>'''
    return svg


def build_code_snippets() -> Dict[str, str]:
    python_fn = (
        "import math\n"
        "def estimate_monolith_gravity(mass_kg: float, distance_m: float) -> float:\n"
        "    \"\"\"Return gravitational acceleration (m/s^2) at a distance from the monolith using Newton's law.\n"
        "    G = 6.67430e-11\n"
        "    return G * mass_kg / (distance_m ** 2)\n\n"
        "def estimate_energy_emission(area_m2: float, emissive_w_per_m2: float) -> float:\n"
        "    \"\"\"Estimate radiant power output (Watts) from a glowing surface.\n"
        "    return area_m2 * emissive_w_per_m2\n"
    )

    kotlin_fn = (
        "import kotlin.math.pow\n\n"
        "object MonolithPhysics {\n"
        "  private const val G: Double = 6.67430e-11\n\n"
        "  fun gravity(massKg: Double, distanceM: Double): Double {\n"
        "    return G * massKg / distanceM.pow(2.0)\n"
        "  }\n\n"
        "  fun energy(areaM2: Double, emissiveWPerM2: Double): Double {\n"
        "    return areaM2 * emissiveWPerM2\n"
        "  }\n"
        "}\n"
    )
    return {"python": python_fn, "kotlin": kotlin_fn}


def build_storyboard(prompt: str) -> List[StoryboardFrame]:
    frames = [
        StoryboardFrame(t=0, title="Approach", description="Camera glides over the lunar terminator into darkness.", camera="slow-dolly-in", elements=["stars", "wireframe spheres", "moon horizon"]).dict(),
        StoryboardFrame(t=10, title="Reveal", description="Electric-blue glow blooms, outlining the monolith.", camera="tilt-up", elements=["monolith", "glow", "regolith dust"]).dict(),
        StoryboardFrame(t=25, title="Inscription", description="Ancient symbols flicker across the obsidian face.", camera="macro-pan", elements=["symbols", "blue runes"]).dict(),
        StoryboardFrame(t=40, title="Distortion", description="Subtle lens warps hint at gravitational shear.", camera="orbit", elements=["gravitational ripple", "ionized haze"]).dict(),
        StoryboardFrame(t=55, title="Contact", description="Astronaut silhouette reaches out as hum crescendos.", camera="push-in", elements=["astronaut", "ribbon light"]).dict(),
    ]
    return frames


def build_audio_layers() -> List[AudioLayer]:
    return [
        AudioLayer(name="Sub Bass Drone", type="drone", waveform="sine", base_freq=41.2, lfo_freq=0.06, reverb=0.6, volume=0.35).
        dict(),
        AudioLayer(name="Iridescent Ribbon", type="pad", waveform="triangle", base_freq=220.0, lfo_freq=0.12, reverb=0.5, volume=0.25).dict(),
        AudioLayer(name="Grain Hiss", type="noisepad", waveform="noise", base_freq=0, lfo_freq=0.2, reverb=0.7, volume=0.15).dict(),
        AudioLayer(name="Beacon Pulses", type="pulse", waveform="sine", notes=[440.0, 554.37, 659.25, 880.0], lfo_freq=0.5, reverb=0.3, volume=0.2).dict(),
    ]


@app.post("/api/hyper-generate", response_model=HyperGenerateResponse)
async def hyper_generate(req: HyperGenerateRequest):
    prompt = req.prompt.strip()
    if not prompt:
        prompt = "A mysterious object radiating faint electric-blue light on the far side of the Moon."

    narration = (
        "On the dark side of the Moon, beyond the reach of Earth's gaze, a monolith rises from the regolith—"
        "its surface black as void, its edges trembling with a faint electric-blue aura. Symbols, older than language,"
        " coil and awaken across its face. Instruments whisper anomalies: gravity bends by imperceptible degrees,"
        " and the static hum resolves into a pattern. This is not a beacon. It is a key—waiting for the question we have yet to ask."
    )

    response: HyperGenerateResponse = HyperGenerateResponse(
        prompt=prompt,
        code_snippets=build_code_snippets(),
        video={
            "duration_sec": 60,
            "narration_text": narration,
            "storyboard": build_storyboard(prompt),
        },
        audio={
            "duration_sec": 300,
            "layers": build_audio_layers(),
        },
        image_svg=build_image_svg(prompt),
        text_response=(
            "The monolith appears to operate as a multi-modal artifact: part gravitational lens, part information lattice. "
            "The faint electric-blue emission suggests controlled energy leakage—possibly a byproduct of field stabilization. "
            "The symbols may not be writing in a human sense but a spatial-temporal indexing scheme; think addresses for aligning matter and memory. "
            "Local perturbations in spacetime hint at a tuned mass effect, allowing the structure to modulate gravity as a carrier wave. "
            "A plausible function is archival: a vault that stores states—maps, genomes, histories—encoded as resonant patterns in vacuum fluctuations. "
            "Contact protocols should avoid RF injection and instead vary inertial frames: micro-thrust oscillations or lattice vibrations on contact surfaces. "
            "If the device is a key, the lock may be planetary: a network expecting the Moon, Earth, and Sun to form precise phase relationships. "
            "In that alignment, the monolith would not open in place; it would redirect—turning the local curvature into a pointer, and us into the message."
        ),
    )

    return response


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
