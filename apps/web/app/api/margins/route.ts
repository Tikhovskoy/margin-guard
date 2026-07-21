import { NextRequest } from "next/server";

const apiUrl = process.env.MARGIN_GUARD_API_URL ?? "http://localhost:8000";

export async function GET(request: NextRequest) {
  const threshold = request.nextUrl.searchParams.get("threshold_percent");
  const query = threshold ? `?threshold_percent=${encodeURIComponent(threshold)}` : "";

  try {
    const response = await fetch(`${apiUrl}/api/v1/margins/preview${query}`, {
      cache: "no-store",
    });
    return new Response(await response.text(), {
      status: response.status,
      headers: { "content-type": response.headers.get("content-type") ?? "application/json" },
    });
  } catch {
    return Response.json({ detail: "Не удалось подключиться к API margin-guard." }, { status: 503 });
  }
}
