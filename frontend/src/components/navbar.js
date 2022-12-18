import { Link, useMatch, useResolvedPath } from "react-router-dom"

export default function Navbar() {
  return (
    <nav className="nav">
      <Link to="/" className="site-title">
        Distributed DB Maker Application
      </Link>
      <ul>
        {/* <CustomLink to="/">About</CustomLink> */}
        <CustomLink to="/localSchema">Create LocalSchema</CustomLink>
        <CustomLink to="/globalSchema">Create GlobalSchema</CustomLink>
        <CustomLink to="/lsRemove">Remove LocalSchema</CustomLink>
        <CustomLink to="/gsRemove">Remove GlobalSchema</CustomLink>


      </ul>
    </nav>
  )
}

function CustomLink({ to, children, ...props }) {
  const resolvedPath = useResolvedPath(to)
  const isActive = useMatch({ path: resolvedPath.pathname, end: true })

  return (
    <li className={isActive ? "active" : ""}>
      <Link to={to} {...props}>
        {children}
      </Link>
    </li>
  )
}

