import type { NextConfig } from "next";

// Read at build time: Vercel sets VERCEL_GIT_COMMIT_SHA during the build, no project toggle needed.
const buildCommit = (process.env.VERCEL_GIT_COMMIT_SHA ?? "dev").slice(0, 7);

const nextConfig: NextConfig = {
  env: {
    BUILD_COMMIT: buildCommit,
  },
  typescript: {
    ignoreBuildErrors: true,
  },
};

export default nextConfig;
