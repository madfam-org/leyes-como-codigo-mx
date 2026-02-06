/** @type {import('next').NextConfig} */
const nextConfig = {
    output: "standalone",
    transpilePackages: ['@leyesmx/ui', '@leyesmx/lib'],
};

export default nextConfig;
