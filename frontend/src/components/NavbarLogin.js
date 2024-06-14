import React from 'react';
import { Link } from 'react-router-dom';

const NavbarLogin = () => {

    
  return (
    <nav className="bg-navbar shadow-lg">
      <div className="max-w-7xl mx-auto px-2 sm:px-6 lg:px-8">
        <div className="relative flex items-center justify-between h-16">
          <h1 className="text-white text-xl font-bold">Company Name</h1>
          <div className="flex items-center">
            <div className="hidden md:block">
              <ul className="flex space-x-4">
                <li>
                  <Link to="/" className="text-white hover:bg-gray-700 px-3 py-2 rounded-md">Login</Link>
                </li>
                <li>
                  <Link to="/about" className="text-white hover:bg-gray-700 px-3 py-2 rounded-md">About</Link>
                </li>
                
              </ul>
            </div>
          </div>
        </div>
      </div>
    </nav>



  );
}

export default NavbarLogin;
