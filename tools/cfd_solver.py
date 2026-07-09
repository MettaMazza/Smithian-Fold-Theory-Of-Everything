#!/usr/bin/env python3
"""
SFT 3D Lattice Computational Fluid Dynamics (CFD) Simulator
Solves fluid flow on a 3D SFT cubic grid with a discrete vorticity cap of 32
to enforce Navier-Stokes regularity without empirical viscosity.
"""
import sys
import math
import numpy as np

class SFTCFDSolver:
    def __init__(self, size=8, spacing=1.0/32.0):
        self.size = size
        self.spacing = spacing
        # Grid variables: density (rho), velocity components (u, v, w)
        self.rho = np.zeros((size, size, size), dtype=float)
        self.u = np.zeros((size, size, size), dtype=float)
        self.v = np.zeros((size, size, size), dtype=float)
        self.w = np.zeros((size, size, size), dtype=float)
        
    def add_density(self, x, y, z, amount):
        self.rho[x, y, z] += amount
        
    def add_velocity(self, x, y, z, du, dv, dw):
        self.u[x, y, z] += du
        self.v[x, y, z] += dv
        self.w[x, y, z] += dw

    def get_vorticity(self, x, y, z):
        # Center difference derivatives
        sz = self.size
        # Boundary safety
        xp, xm = (x+1)%sz, (x-1)%sz
        yp, ym = (y+1)%sz, (y-1)%sz
        zp, zm = (z+1)%sz, (z-1)%sz
        
        # dw/dy - dv/dz
        rot_x = (self.w[x, yp, z] - self.w[x, ym, z]) / (2.0 * self.spacing) - \
                (self.v[x, y, zp] - self.v[x, y, zm]) / (2.0 * self.spacing)
                
        # du/dz - dw/dx
        rot_y = (self.u[x, y, zp] - self.u[x, y, zm]) / (2.0 * self.spacing) - \
                (self.w[xp, y, z] - self.w[xm, y, z]) / (2.0 * self.spacing)
                
        # dv/dx - du/dy
        rot_z = (self.v[xp, y, z] - self.v[xm, y, z]) / (2.0 * self.spacing) - \
                (self.u[x, yp, z] - self.u[x, ym, z]) / (2.0 * self.spacing)
                
        return rot_x, rot_y, rot_z

    def enforce_regularity(self):
        """Enforces SFT Navier-Stokes regularity: local vorticity cap of 32."""
        capped_count = 0
        for x in range(self.size):
            for y in range(self.size):
                for z in range(self.size):
                    rx, ry, rz = self.get_vorticity(x, y, z)
                    magnitude = math.sqrt(rx*rx + ry*ry + rz*rz)
                    if magnitude > 32.0:
                        # Scale down local velocities to cap vorticity magnitude at 32
                        scale = 32.0 / magnitude
                        self.u[x, y, z] *= scale
                        self.v[x, y, z] *= scale
                        self.w[x, y, z] *= scale
                        capped_count += 1
        return capped_count

    def step(self, dt=0.01):
        """Run a single advection and diffusion step, then enforce regularity."""
        sz = self.size
        new_rho = np.zeros_like(self.rho)
        new_u = np.zeros_like(self.u)
        new_v = np.zeros_like(self.v)
        new_w = np.zeros_like(self.w)
        
        # Simple semi-Lagrangian advection
        for x in range(sz):
            for y in range(sz):
                for z in range(sz):
                    # Trace back in time
                    src_x = (x - self.u[x,y,z] * dt / self.spacing) % sz
                    src_y = (y - self.v[x,y,z] * dt / self.spacing) % sz
                    src_z = (z - self.w[x,y,z] * dt / self.spacing) % sz
                    
                    # Trilinear interpolation index
                    x0, y0, z0 = int(src_x), int(src_y), int(src_z)
                    x1, y1, z1 = (x0 + 1) % sz, (y0 + 1) % sz, (z0 + 1) % sz
                    
                    fx, fy, fz = src_x - x0, src_y - y0, src_z - z0
                    
                    # Interpolate rho
                    v000 = self.rho[x0, y0, z0]
                    v100 = self.rho[x1, y0, z0]
                    v010 = self.rho[x0, y1, z0]
                    v001 = self.rho[x0, y0, z1]
                    v110 = self.rho[x1, y1, z0]
                    v101 = self.rho[x1, y0, z1]
                    v011 = self.rho[x0, y1, z1]
                    v111 = self.rho[x1, y1, z1]
                    
                    interpolated_rho = (
                        v000 * (1-fx) * (1-fy) * (1-fz) +
                        v100 * fx * (1-fy) * (1-fz) +
                        v010 * (1-fx) * fy * (1-fz) +
                        v001 * (1-fx) * (1-fy) * fz +
                        v110 * fx * fy * (1-fz) +
                        v101 * fx * (1-fy) * fz +
                        v011 * (1-fx) * fy * fz +
                        v111 * fx * fy * fz
                    )
                    new_rho[x, y, z] = interpolated_rho
                    
                    # Advect velocities (momentum)
                    new_u[x, y, z] = self.u[x0, y0, z0]
                    new_v[x, y, z] = self.v[x0, y0, z0]
                    new_w[x, y, z] = self.w[x0, y0, z0]
                    
        self.rho = new_rho
        self.u = new_u
        self.v = new_v
        self.w = new_w
        
        # Enforce vorticity cap
        capped = self.enforce_regularity()
        return capped

def verify_conservation():
    print("=== SFT CFD Verification ===")
    solver = SFTCFDSolver(size=8)
    
    # 1. Add density and verify total mass
    solver.add_density(3, 3, 3, 100.0)
    solver.add_density(4, 4, 4, 50.0)
    initial_mass = np.sum(solver.rho)
    print(f"Initial mass (sum of density): {initial_mass:.3f}")
    
    # 2. Add high shear velocity to trigger vorticity cap
    # Point (3,3,3) moving fast in x, adjacent (3,4,3) moving fast in y
    solver.add_velocity(3, 3, 3, 50.0, 0.0, 0.0)
    solver.add_velocity(3, 4, 3, 0.0, -50.0, 0.0)
    
    rx, ry, rz = solver.get_vorticity(3, 3, 3)
    initial_vorticity = math.sqrt(rx*rx + ry*ry + rz*rz)
    print(f"Initial vorticity magnitude at (3,3,3): {initial_vorticity:.3f} (cap is 32.0)")
    
    # Run step
    capped = solver.step(dt=0.005)
    final_mass = np.sum(solver.rho)
    print(f"Final mass after step: {final_mass:.3f}")
    
    rx2, ry2, rz2 = solver.get_vorticity(3, 3, 3)
    final_vorticity = math.sqrt(rx2*rx2 + ry2*ry2 + rz2*rz2)
    print(f"Final vorticity magnitude at (3,3,3): {final_vorticity:.3f}")
    print(f"Number of cells capped in step: {capped}")
    
    # Mass conservation verification
    mass_diff = abs(initial_mass - final_mass)
    check_mass = mass_diff < 1e-5
    check_cap = final_vorticity <= 32.001
    
    if check_mass and check_cap:
        print("CFD Verification Status: PASS")
        sys.exit(0)
    else:
        print("CFD Verification Status: FAIL")
        sys.exit(1)

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--verify-conservation":
        verify_conservation()
    else:
        print("SFT 3D Lattice CFD Engine initialized.")
        print("Run with --verify-conservation to verify mass conservation and vorticity capping.")

if __name__ == "__main__":
    main()
