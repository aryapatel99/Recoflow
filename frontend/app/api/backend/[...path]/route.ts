import { NextRequest, NextResponse } from "next/server";

const configuredBackendUrl = process.env.NEXT_PUBLIC_API_URL;
if (process.env.NODE_ENV === "production" && !configuredBackendUrl) {
  throw new Error("NEXT_PUBLIC_API_URL must be configured for production builds.");
}

const BACKEND_URL = configuredBackendUrl || "http://127.0.0.1:8000";

async function forward(
  request: NextRequest,
  { params }: { params: Promise<{ path: string[] }> },
) {
  const { path } = await params;
  const target = `${BACKEND_URL}/${path.join("/")}${request.nextUrl.search}`;
  const headers = new Headers(request.headers);
  headers.delete("host");
  headers.delete("content-length");

  try {
    const response = await fetch(target, {
      method: request.method,
      headers,
      body:
        request.method === "GET" || request.method === "HEAD"
          ? undefined
          : await request.arrayBuffer(),
      cache: "no-store",
    });

    return new NextResponse(response.body, {
      status: response.status,
      headers: {
        "content-type":
          response.headers.get("content-type") || "application/json",
      },
    });
  } catch {
    return NextResponse.json(
      { detail: "Backend request could not be completed." },
      { status: 502 },
    );
  }
}

export const GET = forward;
export const POST = forward;
export const PUT = forward;
export const PATCH = forward;
export const DELETE = forward;
