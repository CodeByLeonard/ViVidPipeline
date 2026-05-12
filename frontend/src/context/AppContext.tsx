import { createContext, useContext, useState, type ReactNode } from "react"

type AppContextType = {
    currentPage: string
    setCurrentPage: (page: string) => void

    youtubeId: string
    setYoutubeId: (id: string) => void

    file: File | null
    setFile: (file: File | null) => void

    clip_file: string
    setClipFile: (path: string) => void

    original_file: string
    setOriginalFile: (path: string) => void
}

const AppContext = createContext<AppContextType | null>(null)

export function AppProvider({ children }: { children: ReactNode }) {
    const [currentPage, setCurrentPage] = useState("Input")
    const [youtubeId, setYoutubeId] = useState("")
    const [file, setFile] = useState<File | null>(null)

    const [clip_file, setClipFile] = useState("Session not initialized")
    const [original_file, setOriginalFile] = useState("Session not initialized")

    return (
        <AppContext.Provider
            value={{
                currentPage, setCurrentPage,
                youtubeId, setYoutubeId,
                file, setFile,

                clip_file, setClipFile,
                original_file, setOriginalFile
            }}
        >
            {children}
        </AppContext.Provider>
    )
}

export function useAppContext() {
    const context = useContext(AppContext)
    if (!context) throw new Error("useAppContext must be used inside AppProvider")
    return context
}