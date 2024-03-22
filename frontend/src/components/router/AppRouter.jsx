import { createBrowserRouter } from 'react-router-dom';
import Login from '../login/login';
import Patient from '../patient/Patient';
import Prescriber from '../prescriber/Prescriber';
import Verification from '../admin/verification/Verification';
import Profiles from '../admin/profiles/Profiles';
import Admin from '../admin/Admin';
import MyPrescriptions from '../prescriber/my-prescriptions/MyPrescriptions';
import { Navigate } from 'react-router-dom';

const router = createBrowserRouter([
    {
      path: "/",
      children: [
        {
          path: "login",
          element: <Login />,
        },
        {
          path: "admin",
          element: <Admin />,
          children: [
            { 
              index: true,
              element: <Navigate to="verification" replace /> 
            }, 
            {
              path: "verification",
              element: <Verification />,
            },
            {
              path: "profiles",
              element: <Profiles />,
            },
          ]
        },
        {
          path: "patient",
          element: <Patient />,
          children: [
            { 
              index: true,
              element: <Navigate to="my-prescriptions" replace /> 
            }, 
            {
              path: "my-prescriptions",
              element: <Verification />,
            },
            {
              path: "green-resources",
              element: <Profiles />,
            },
          ]
        },
        {
          path: "prescriber",
          element: <Prescriber />,
          children: [
            { 
              index: true,
              element: <Navigate to="my-prescriptions" replace /> 
            }, 
            {
              path: "my-prescriptions",
              element: <MyPrescriptions />,
            },
            {
              path: "green-resources",
              element: <Profiles />,
            },
          ]
        },
      ],
    },
  ]);

const AppRouter = () => {
  return router;
};

export default AppRouter;