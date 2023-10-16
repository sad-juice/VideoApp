import HomeIcon from '@mui/icons-material/Home';
import PeopleIcon from '@mui/icons-material/People';
import PublicIcon from '@mui/icons-material/Public';

export const NavbarItems = [
    {
        id: 0,
        icon: <HomeIcon />,
        label: 'Home',
        route: '/',
    },
    {
        id: 1,
        icon: <PeopleIcon />,
        label: 'Page1',
        route: 'page1',
    },
    {
        id: 2,
        icon: <PublicIcon />,
        label: 'Page2',
        route: 'page2',
    },
]