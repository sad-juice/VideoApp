import Layout from "./components/Layout";
import Home from "./pages/Home";
import Page1 from "./pages/Page1";
import Page2 from "./pages/Page2";
import Login from "./pages/Login";
import Signup from "./pages/Signup";
import { createBrowserRouter, Route, createRoutesFromElements, RouterProvider, Navigate } from "react-router-dom";
import useAuthContext from "./hooks/useAuthContext";


function App() {
  const { user } = useAuthContext()

  const router = createBrowserRouter(

    createRoutesFromElements(
      <Route path="/" element={<Layout />}>
        <Route exact index element={ user ? <Home /> : <Navigate to="/login" />} />
        <Route exact path="page1" element={ user ? <Page1 /> : <Navigate to="/login" />} />
        <Route exact path="page2" element={ user ? <Page2 /> : <Navigate to="/login" />} />
        <Route exact path="login" element={ !user ? <Login /> : <Navigate to="/" />} />
        <Route exact path="signup" element={ !user ? <Signup /> : <Navigate to="/" />} />
      </Route> 
    )
  )
  
  return (
    <div className="App">
      <RouterProvider router={router} />
    </div>
  );
}

export default App;