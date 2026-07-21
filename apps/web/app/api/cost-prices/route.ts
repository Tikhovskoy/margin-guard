const apiUrl = process.env.MARGIN_GUARD_API_URL ?? "http://localhost:8000";

export async function POST(request: Request) {
  try {
    const formData = await request.formData();
    const response = await fetch(`${apiUrl}/api/v1/cost-prices/upload`, {
      method: "POST",
      body: formData,
    });
    return new Response(await response.text(), {
      status: response.status,
      headers: { "content-type": response.headers.get("content-type") ?? "application/json" },
    });
  } catch {
    return Response.json({ detail: "Не удалось подключиться к API margin-guard." }, { status: 503 });
  }
}
