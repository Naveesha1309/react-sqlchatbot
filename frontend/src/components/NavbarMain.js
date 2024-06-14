import React from 'react';
import { Link } from 'react-router-dom';
import { AuthContext } from './AuthContext';
import { useContext } from 'react';
import { useNavigate } from 'react-router-dom';

const NavbarMain = () => {

  const { isLoggedIn, logout } = useContext(AuthContext);
    const navigate = useNavigate();

    const handleLogout = () => {
        logout();
        navigate('/');
    };
  return (
    <nav className="shadow-lg bg-navbar">
  <div className="max-w-7xl mx-auto px-2 sm:px-6 lg:px-8">
    <div className="relative flex items-center justify-between h-16">
      <h1 className="text-white text-xl font-bold">Company Name</h1>
      <div className="hidden md:flex items-center space-x-4"> {/* Updated here */}
        {isLoggedIn && (
          <button onClick={handleLogout} className="text-white hover:bg-gray-700 px-3 py-2 rounded-md">Logout</button>
        )}
        <Link to="/about" className="text-white hover:bg-gray-700 px-3 py-2 rounded-md">About</Link>
        {/* Add more navigation items as needed */}
      </div>
    </div>
  </div>
</nav>

  );
}

export default NavbarMain;
