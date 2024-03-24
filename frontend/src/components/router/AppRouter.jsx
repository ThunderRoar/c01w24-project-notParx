import { createBrowserRouter } from 'react-router-dom';
import Login from '../login/login';
import Patient from '../patient/Patient';
import Prescriber from '../prescriber/Prescriber';
import Verification from '../admin/verification/Verification';
import Profiles from '../admin/profiles/Profiles';
import Admin from '../admin/Admin';
import PrescriberPrescriptions from '../prescriber/my-prescriptions/PrescriberPrescriptions';
import { Navigate } from 'react-router-dom';
import PatientPrescriptions from '../patient/my-prescriptions/PatientPrescriptions';

const router = createBrowserRouter([
    {
      path: "/",
      children: [
        {
          path: "",
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
              element: <PatientPrescriptions />,
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
              element: <PrescriberPrescriptions />,
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