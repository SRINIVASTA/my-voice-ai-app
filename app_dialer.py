import asyncio
import random
from modules.database import init_db, save_log

# Target lead list data arrays
phone_list = [f"+9198765432{i:02d}" for i in range(1, 16)]

telugu_citizen_inputs = [
    "Yes, I received the pension on time.",
    "No, the official came two days late.",
    "The process was smooth, thank you.",
    "I had to submit my documents twice.",
    "Everything is working perfectly fine.",
    "There was an error in my transaction."
]

async def simulate_call_session(phone, slot_id):
    """Asynchronously drives distinct parallel calling threads with a 60s hard ceiling."""
    await asyncio.sleep(random.uniform(0.5, 1.5))
    is_answered = random.choices([True, False], weights=[0.85, 0.15])[0]
    
    if not is_answered:
        save_log(f"Slot {slot_id:02d}", phone, "No Answer", 0, "N/A")
        return

    # Simulate individual call length execution metrics under a strict 60s rule
    duration = random.choice([15, 30, 45, 60]) 
    status = "Completed (Max Limit)" if duration == 60 else "Citizen Hung Up Early"
    speech_captured = random.choice(telugu_citizen_inputs)
    
    save_log(f"Slot {slot_id:02d}", phone, status, duration, speech_captured)

async def main():
    init_db()
    print("🚀 Initializing SQLite and firing concurrent mock channels...")
    tasks = [simulate_call_session(num, idx + 1) for idx, num in enumerate(phone_list)]
    await asyncio.gather(*tasks)
    print("🏁 Call processing batch completely saved to database file.")

if __name__ == "__main__":
    asyncio.run(main())
