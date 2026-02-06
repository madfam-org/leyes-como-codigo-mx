import { createJanuaMiddleware } from "@janua/nextjs/server";

export default createJanuaMiddleware({
    publicRoutes: ["/sign-in", "/api/health"],
    signInUrl: "/sign-in",
});

export const config = {
    matcher: [
        // Match all routes except Next.js internals and static files
        "/((?!_next|[^?]*\\.(?:html?|css|js(?!on)|jpe?g|webp|png|gif|svg|ttf|woff2?|ico|csv|docx?|xlsx?|zip|webmanifest)).*)",
    ],
};
