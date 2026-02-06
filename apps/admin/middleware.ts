import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

let middleware: (req: NextRequest) => ReturnType<typeof NextResponse.next>;

try {
    // eslint-disable-next-line @typescript-eslint/no-require-imports
    const { createJanuaMiddleware } = require("@janua/nextjs/server");
    middleware = createJanuaMiddleware({
        publicRoutes: ["/sign-in", "/api/health"],
        signInUrl: "/sign-in",
    });
} catch {
    // @janua/nextjs not installed — allow all requests through
    middleware = () => NextResponse.next();
}

export default function handler(req: NextRequest) {
    return middleware(req);
}

export const config = {
    matcher: [
        "/((?!_next|[^?]*\\.(?:html?|css|js(?!on)|jpe?g|webp|png|gif|svg|ttf|woff2?|ico|csv|docx?|xlsx?|zip|webmanifest)).*)",
    ],
};
