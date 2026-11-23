
import { Component, inject, ChangeDetectorRef } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Router } from '@angular/router';

interface LoginResponse {
  access_token: string;
  token_type: string;
  usuario: {
    id: number;
    email: string;
    nombre: string;
    rol: string;
  };
}

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [FormsModule],
  templateUrl: './login.html',
  styleUrl: './login.scss'
})
export class Login {

  private http = inject(HttpClient);
  private router = inject(Router);
  private cdr = inject(ChangeDetectorRef);

  email = '';
  password = '';
  cargando = false;
  error = '';

  iniciarSesion(): void {

    if (this.cargando) {
      return;
    }

    this.error = '';
    this.cargando = true;

    this.http.post<LoginResponse>(
      'http://127.0.0.1:8000/auth/login',
      {
        email: this.email,
        password: this.password
      }
    ).subscribe({

      next: (respuesta) => {
        this.cargando = false;

        sessionStorage.setItem(
          'ecogestion_token',
          respuesta.access_token
        );

        this.cdr.markForCheck();
        this.router.navigate(['/dashboard']);
      },

      error: (err: HttpErrorResponse) => {
        this.cargando = false;

        if (err.status === 401) {
          this.error = 'Correo o contraseña incorrectos.';
        } else if (err.status === 0) {
          this.error = 'No se pudo conectar con FastAPI.';
        } else {
          this.error = 'Error del servidor. Código: ' + err.status;
        }

        this.cdr.markForCheck();
      }

    });
  }
}
