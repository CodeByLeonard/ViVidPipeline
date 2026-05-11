import {type ReactNode, useState} from "react";
import {initializeSession, resetSession} from "../modules/BackendHelper.tsx";
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

const glassPanel = "bg-white/5 backdrop-blur-xl border border-white/10 shadow-[0_8px_32px_rgba(0,0,0,0.35)]"
const headerSpacing = "relative flex items-center px-6"
const headerElement = "flex items-center gap-3"

function Header({children}: { children: ReactNode }) {
    return <header className={ `w-[95%] h-16 rounded-2xl ${glassPanel} ${headerSpacing}` }> {children} </header>
}

function Left() {
    const orb = "w-8 h-8 rounded-lg bg-linear-to-br from-cyan-400 to-blue-500 shadow-lg shadow-cyan-500/20"
    const leftModule = `${headerElement} z-10`
    return (
        <div className={leftModule}>
            <div className={orb}/>
            <div className="flex flex-col">
                <span className="text-sm text-zinc-400">Audio Engineering</span>
                <span className="text-white font-semibold tracking-wide">Reconstruction Suite</span>
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
                <NavButton key={item} label={item} active={currentPage === item} onClick={() => setCurrentPage(item)}/>
            ))}
        </nav>
    )
}

function Right() {
    const [loading, setLoading] = useState(false)
    const { setCurrentPage, youtubeId, file} = useAppContext()

    const rightModule = `${headerElement} ml-auto z-10`

    const initializeGlassPanel = "bg-white/5 backdrop-blur-xl border border-white/10 shadow-[0_8px_32px_rgba(0,0,0,0.35)]"
    const initializeButton = `px-4 py-2 rounded-xl ${initializeGlassPanel} hover:bg-white/10 text-zinc-200 text-sm transition`
    const disabledButton = "opacity-50 cursor-not-allowed hover:bg-zinc-800/60"

    const resetGlassPanel = "bg-red-500/5 backdrop-blur-xl border border-white/10 shadow-[0_4px_32px_rgba(140,0,0,0.35)]"
    const resetButton = `px-4 py-2 rounded-xl ${resetGlassPanel} hover:bg-red-500/10 text-red-200 text-sm transition`

    return (
        <div className={rightModule}>
            <button onClick={() => initializeSession({youtubeId, file, setLoading, setCurrentPage})}
                    className={initializeButton + (loading ? " " + disabledButton : " hover:bg-zinc-700/40")}
                    disabled={loading}>
                {loading ? "Initializing Session" : "Initialize Session"}
            </button>
            <button onClick={resetSession} className={resetButton}> Reset Session </button>
        </div>
    )
}

function NavButton({label, active = false, onClick}: {
    label: string
    active?: boolean
    onClick?: () => void
})
{
    const activeStyles = `bg-white/10 text-white shadow-lg`
    const inactiveStyles = `text-zinc-400 hover:text-white hover:bg-white/5`
    const navButton = `px-4 py-2 rounded-xl text-sm transition-all ${active ? activeStyles : inactiveStyles}`
    return <button onClick={onClick} className={navButton}>{label}</button>
}