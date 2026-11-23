
import { Component, OnInit, inject, signal, computed } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Router } from '@angular/router';
import { forkJoin } from 'rxjs';

interface TipoMaterial {
  id: number;
  nombre: string;
}

interface Recoleccion {
  id: number;
  familia_id: number;
  familia_nombre?: string;
  fecha: string;
  estado: string;
}

interface RegistroMaterial {
  id: number;
  recoleccion_id: number;
  material_id: number;
  cantidad_kg: number;
  fecha_registro: string;
}

@Component({
  selector: 'app-materiales',
  standalone: true,
  imports: [FormsModule],
  templateUrl: './materiales.html',
  styleUrl: './materiales.scss'
})
export class Materiales implements OnInit {

  private http = inject(HttpClient);
  private router = inject(Router);

  private apiUrl = 'http://127.0.0.1:8000';

  materiales = signal<RegistroMaterial[]>([]);
  tiposMaterial = signal<TipoMaterial[]>([]);
  recolecciones = signal<Recoleccion[]>([]);

  recoleccionesCompletadas = computed(() =>
    this.recolecciones().filter(
      r => r.estado === 'completada'
    )
  );

  cargando = signal(false);
  guardando = signal(false);
  mostrarFormulario = signal(false);

  editandoId = signal<number | null>(null);
  eliminandoId = signal<number | null>(null);

  error = signal('');
  mensaje = signal('');

  formulario = {
    recoleccion_id: 0,
    material_id: 0,
    cantidad_kg: 0,
    fecha_registro: ''
  };

  ngOnInit(): void {
    this.cargarDatos();
  }

  private obtenerHeaders(): HttpHeaders | null {
    const token = sessionStorage.getItem('ecogestion_token');

    if (!token) {
      this.router.navigate(['/login']);
      return null;
    }

    return new HttpHeaders({
      Authorization: `Bearer ${token}`
    });
  }

  private manejarError(status: number, texto: string): void {
    if (status === 401) {
      sessionStorage.removeItem('ecogestion_token');
      this.router.navigate(['/login']);
      return;
    }

    this.error.set(`${texto} Código: ${status}`);
  }

  // CONSULTAR materiales, tipos y recolecciones
  cargarDatos(): void {
    const headers = this.obtenerHeaders();
    if (!headers) return;

    this.cargando.set(true);
    this.error.set('');

    forkJoin({
      materiales: this.http.get<RegistroMaterial[]>(
        `${this.apiUrl}/materiales`,
        { headers }
      ),
      tipos: this.http.get<TipoMaterial[]>(
        `${this.apiUrl}/tipos-material`,
        { headers }
      ),
      recolecciones: this.http.get<Recoleccion[]>(
        `${this.apiUrl}/recolecciones`,
        { headers }
      )
    }).subscribe({
      next: (datos) => {
        this.materiales.set(datos.materiales);
        this.tiposMaterial.set(datos.tipos);
        this.recolecciones.set(datos.recolecciones);
        this.cargando.set(false);
      },
      error: (err) => {
        this.cargando.set(false);
        this.manejarError(
          err.status,
          'No se pudieron cargar los materiales.'
        );
      }
    });
  }

  nombreMaterial(id: number): string {
    return this.tiposMaterial().find(
      tipo => tipo.id === id
    )?.nombre ?? `Material #${id}`;
  }

  nombreFamilia(recoleccionId: number): string {
    const r = this.recolecciones().find(
      item => item.id === recoleccionId
    );

    return r?.familia_nombre ?? `Recolección #${recoleccionId}`;
  }

  // CREAR nuevo registro
  abrirFormulario(): void {
    this.editandoId.set(null);

    this.formulario = {
      recoleccion_id: 0,
      material_id: 0,
      cantidad_kg: 0,
      fecha_registro: ''
    };

    this.error.set('');
    this.mensaje.set('');
    this.mostrarFormulario.set(true);
  }

  // EDITAR registro existente
  editarMaterial(material: RegistroMaterial): void {
    this.editandoId.set(material.id);

    this.formulario = {
      recoleccion_id: material.recoleccion_id,
      material_id: material.material_id,
      cantidad_kg: Number(material.cantidad_kg),
      fecha_registro: material.fecha_registro
    };

    this.error.set('');
    this.mensaje.set('');
    this.mostrarFormulario.set(true);
  }

  cancelarFormulario(): void {
    this.mostrarFormulario.set(false);
    this.editandoId.set(null);
    this.error.set('');
  }

  // GUARDAR mediante POST o PUT
  guardarMaterial(): void {
    const headers = this.obtenerHeaders();
    if (!headers || this.guardando()) return;

    const datos = {
      recoleccion_id: Number(this.formulario.recoleccion_id),
      material_id: Number(this.formulario.material_id),
      cantidad_kg: Number(this.formulario.cantidad_kg),
      fecha_registro: this.formulario.fecha_registro
    };

    if (
      !datos.recoleccion_id ||
      !datos.material_id ||
      !datos.fecha_registro ||
      !Number.isFinite(datos.cantidad_kg) ||
      datos.cantidad_kg <= 0
    ) {
      this.error.set(
        'Completa todos los campos y coloca una cantidad mayor a cero.'
      );
      return;
    }

    const id = this.editandoId();

    this.guardando.set(true);
    this.error.set('');

    const solicitud = id !== null
      ? this.http.put<RegistroMaterial>(
          `${this.apiUrl}/materiales/${id}`,
          datos,
          { headers }
        )
      : this.http.post<RegistroMaterial>(
          `${this.apiUrl}/materiales`,
          datos,
          { headers }
        );

    solicitud.subscribe({
      next: () => {
        this.guardando.set(false);
        this.mostrarFormulario.set(false);
        this.editandoId.set(null);

        this.mensaje.set(
          id !== null
            ? 'Material actualizado correctamente.'
            : 'Material registrado correctamente.'
        );

        this.cargarDatos();
      },
      error: (err) => {
        this.guardando.set(false);

        this.manejarError(
          err.status,
          'No se pudo guardar el material.'
        );
      }
    });
  }

  // ELIMINAR registro
  eliminarMaterial(material: RegistroMaterial): void {
    if (this.eliminandoId() !== null) return;

    const confirmar = window.confirm(
      `¿Deseas eliminar el registro de ${this.nombreMaterial(material.material_id)}?`
    );

    if (!confirmar) return;

    const headers = this.obtenerHeaders();
    if (!headers) return;

    this.eliminandoId.set(material.id);
    this.error.set('');
    this.mensaje.set('');

    this.http.delete<void>(
      `${this.apiUrl}/materiales/${material.id}`,
      { headers }
    ).subscribe({
      next: () => {
        this.eliminandoId.set(null);
        this.mensaje.set('Material eliminado correctamente.');
        this.cargarDatos();
      },
      error: (err) => {
        this.eliminandoId.set(null);

        this.manejarError(
          err.status,
          'No se pudo eliminar el material.'
        );
      }
    });
  }

  volverDashboard(): void {
    this.router.navigate(['/dashboard']);
  }
}
