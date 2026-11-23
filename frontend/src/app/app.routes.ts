
import { Routes } from '@angular/router';

import { Login } from './pages/login/login';
import { Dashboard } from './pages/dashboard/dashboard';
import { Familias } from './pages/familias/familias';
import { Recolecciones } from './pages/recolecciones/recolecciones';
import { Materiales } from './pages/materiales/materiales';

import { authGuard } from './guards/auth.guard';

export const routes: Routes = [
  {
    path: '',
    redirectTo: 'login',
    pathMatch: 'full'
  },
  {
    path: 'login',
    component: Login
  },
  {
    path: 'dashboard',
    component: Dashboard,
    canActivate: [authGuard]
  },
  {
    path: 'familias',
    component: Familias,
    canActivate: [authGuard]
  },
  {
    path: 'recolecciones',
    component: Recolecciones,
    canActivate: [authGuard]
  },
  {
    path: 'materiales',
    component: Materiales,
    canActivate: [authGuard]
  },
  {
    path: '**',
    redirectTo: 'login'
  }
];
