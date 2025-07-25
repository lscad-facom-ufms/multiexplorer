/// <reference types="vite/client" />

interface ImportMeta {
    readonly env: ImportMetaEnv
}

interface ImportMetaEnv {
    readonly VITE_SENTRY_DSN: string
}