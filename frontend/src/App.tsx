import Navigation from "./components/Navigation.tsx"
import InputPage from "./pages/InputPage.tsx";
import ScopePage from "./pages/ScopePage.tsx";
import MatchingPage from "./pages/MatchingPage.tsx";
import OutputPage from "./pages/OutputPage.tsx";
import {useAppContext} from "./context/AppContext.tsx";

export default function App() {
    const { currentPage } = useAppContext()
    const navItems: string[] = [ "Input", "Scope", "Matching", "Output" ]

    return (
        <div className="w-screen h-screen bg-[#0b0f14] overflow-hidden relative">
            <Navigation navItems={navItems}/>

            <main className="absolute inset-0 pt-20">
                {currentPage === "Input" && <InputPage/>}
                {currentPage === "Scope" && <ScopePage />}
                {currentPage === "Matching" && <MatchingPage />}
                {currentPage === "Output" && <OutputPage />}
            </main>
        </div>
    )
}