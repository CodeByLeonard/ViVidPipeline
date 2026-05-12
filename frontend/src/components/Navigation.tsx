import {type ReactNode, useState} from "react";
import {initializeSession, resetSession, type SessionInitializer} from "../modules/BackendHelper.tsx";
import {useAppContext} from "../context/AppContext.tsx";

export default function Navigation({navItems}: {navItems: string[] }) {
    return (
        <div className="w-full flex justify-center pt-4 absolute top-0 left-0 z-50">
            <Header>
                <Left/>
                <Center navItems={navItems} />
                <Right />
            </Header>
        </div>
    )
}

const buttonsClickable = true
const glassPanel = "bg-white/5 backdrop-blur-xl border border-white/10 shadow-[0_8px_32px_rgba(0,0,0,0.35)]"
const headerSpacing = "relative flex items-center px-6"
const headerElement = "flex items-center gap-3"

function Header({children}: { children: ReactNode }) {
    return <header className={ `w-[95%] h-16 rounded-2xl ${glassPanel} ${headerSpacing}` }> {children} </header>
}

function Left() {
    const leftModule = `${headerElement} z-10`
    const orb = "w-8 h-8 rounded-lg bg-linear-to-br from-gray-200 to-red-500 shadow-lg shadow-red-500/20" //from-cyan-400 to-blue-500 shadow-cyan-500/20"
    return (
        <div className={leftModule}>
            <div className={orb}/>
            <div className="flex flex-col">
                <span className="text-sm text-zinc-400">ViVidPipeline</span>
                <span className="text-white font-semibold tracking-wide">Shorts Reverse Engineering</span>
            </div>
        </div>
    )
}

function Center({navItems}: {navItems: string[]}) {
    const { currentPage, setCurrentPage} = useAppContext()
    const centerModule = `${headerElement} bg-black/20 border border-white/5 rounded-xl p-1 absolute left-1/2 -translate-x-1/2`
    return (
        <nav className={centerModule}>
            {navItems.map((item) => (
                <NavButton key={item} label={item} active={currentPage === item}
                onClick={(buttonsClickable ? () => {setCurrentPage(item)} : () => {})}/>
            ))}
        </nav>
    )
}

function Right() {
    const rightModule = `${headerElement} ml-auto z-10`

    const initializeGlassPanel = "bg-white/5 backdrop-blur-xl border border-white/10 shadow-[0_8px_32px_rgba(0,0,0,0.35)]"
    const initializeButton = `px-4 py-2 rounded-xl ${initializeGlassPanel} hover:bg-white/10 text-zinc-200 text-sm transition`
    const disabledButton = "opacity-50 cursor-not-allowed hover:bg-zinc-800/60"

    const resetGlassPanel = "bg-red-500/5 backdrop-blur-xl border border-white/10 shadow-[0_4px_32px_rgba(140,0,0,0.35)]"
    const resetButton = `px-4 py-2 rounded-xl ${resetGlassPanel} hover:bg-red-500/10 text-red-200 text-sm transition`

    const [loading, setLoading] = useState(false)
    const { currentPage, setCurrentPage, original_file, setOriginalFile, clip_file, setClipFile } = useAppContext()
    const { youtubeId, file } = useAppContext()
    const initializer: SessionInitializer = {
        youtubeId: youtubeId,
        file: file,
        setLoading: setLoading,
        setCurrentPage: setCurrentPage,
        setOriginalFile: setOriginalFile,
        setClipFile: setClipFile,
    }

    return (
        <div className={rightModule}>
            { currentPage == "Input"
                ? <button onClick={() => initializeSession(initializer)}
                            className={initializeButton + (loading ? " " + disabledButton : " hover:bg-zinc-700/40")}
                            disabled={loading}>
                      {loading ? "Initializing Session" : "Initialize Session"}
                  </button>
                :
                <>
                    <button className={initializeButton}>Clip: {clip_file}</button>
                    <button className={initializeButton}>Original: {original_file}</button>
                    <button onClick={resetSession} className={resetButton}> Reset Session </button>
                </>
            }
        </div>
    )
}


function NavButton({label, active = false, onClick}: { label: string, active?: boolean, onClick?: () => void }) {
    const activeStyles = `bg-white/10 text-white shadow-lg`
    const inactiveStyles = `text-zinc-400 hover:text-white hover:bg-white/5`
    const navButton = `px-4 py-2 rounded-xl text-sm transition-all ${active ? activeStyles : inactiveStyles}`
    if (buttonsClickable) return <button onClick={onClick} className={navButton}>{label}</button>
    else return <button className={`px-4 py-2 rounded-xl text-sm transition-all ${active ? activeStyles : `text-zinc-400`}`}>{label}</button>
}