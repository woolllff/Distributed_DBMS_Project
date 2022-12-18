import Navbar from "./components/navbar"
import { Route, Routes } from "react-router-dom"
import GlobalSchemaMaker from "./components/createGS"
import LocalSchemaMaker from "./components/createLS"
import About from "./components/DDBApp"
import GlobalSchemaRemover from "./components/deleteGS"
import LocalSchemaRemover from "./components/deleteLS"

function App() {
  return (
    <>
      <Navbar />
      <div className="container">
        <Routes>
          <Route path="/" element={<About />} />
          <Route path="/localSchema" element={<LocalSchemaMaker />} />
          <Route path="/globalSchema" element={<GlobalSchemaMaker />} />
          <Route path="/lsRemove" element={<LocalSchemaRemover />} />
          <Route path="/gsRemove" element={<GlobalSchemaRemover />} />
          
          
        </Routes>
      </div>
    </>
  )
}

export default App