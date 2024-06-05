from flask import jsonify
import json
from openai import OpenAI, AssistantEventHandler


def getPrompt():
    tinggi_badan = 97.5
    usia = 24
    status = 'stunted,overweight'
    berat_badan = 65
    jenis_kelamin = 'laki-laki'
    client = OpenAI()

    # Create a new thread
    thread = client.beta.threads.create()
    input_message = 'tinggi badan: {}, usia: {} tahun, status_gizi:{}, berat badan:{}, jenis kelamin:{}'.format(
        tinggi_badan, usia / 12, status, berat_badan, jenis_kelamin
    )

    message = client.beta.threads.messages.create(
        thread_id=thread.id, role='user', content=input_message
    )

    # Define the instructions for the assistant
    instructions = 'Berikan rekomendasi makanan anak - anak berdasarkan input. tampilkan berupa list dan juga berikan rekomendasi penanganannya'

    assistant = client.beta.assistants.create(
        name='StuntShield Doctor',
        instructions=instructions,
        model='gpt-4o',
    )
    run = client.beta.threads.runs.create_and_poll(
        thread_id=thread.id,
        assistant_id=assistant.id,
        instructions='sebutkan usia, tinggi badan, berat badan, jenis kelamin, status gizi terlebih dahulu, lalu Berikan rekomendasi makanan anak - anak berdasarkan input. tampilkan berupa list dan juga berikan rekomendasi penanganannya',
    )

    messages = 'gagal membuat rekomendasi.'
    if run.status == 'completed':
        messages = client.beta.threads.messages.list(thread_id=thread.id)
        messages = messages.data[0].content[0].text.value
    return jsonify({'success': 'OK', 'message': str(messages)}), 200
