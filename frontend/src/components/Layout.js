import React from 'react';
import NavbarMain from './NavbarMain';
import Footer from './Footer';

const Layout = ({ children }) => {
    return (
        <>
            <NavbarMain />
            <div className="min-h-screen bg-cover bg-center" style={{ backgroundImage: 'url(https://images.pexels.com/photos/8721318/pexels-photo-8721318.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2)' }}>
        <main>{children}</main>
            </div>
            
            <Footer />
        </>
    );
};

export default Layout;

// bg opt: https://images.pexels.com/photos/924824/pexels-photo-924824.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2
