import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { AuthenticationService } from '../authentication.service';
import { MatSnackBar } from '@angular/material/snack-bar';
import { Observable } from 'rxjs';
import { Applicant } from './organization.model';

@Injectable({
  providedIn: 'root'
})
export class ApplicantService {
  constructor(
    protected http: HttpClient,
    protected auth: AuthenticationService,
    protected snackBar: MatSnackBar
  ) {}

  // Returns all pending applications for a given organization
  getApplicants(slug: string): Observable<Applicant[]> {
    return this.http.get<Applicant[]>('/api/applicants/' + slug);
  }

  // Returns an application from its id
  getApplicant(id: number): Observable<Applicant> {
    return this.http.get<Applicant>('/api/applicants/' + 'id/' + id);
  }

  // Returns the new application object
  createApplicant(slug: string, application: Applicant): Observable<Applicant> {
    return this.http.post<Applicant>('/api/applicants/' + slug, application);
  }

  // Returns the updated application object
  updateApplicant(id: number, application: Applicant): Observable<Applicant> {
    return this.http.put<Applicant>('/api/applicants/' + id, application);
  }

  // Removes application object
  removeApplicant(id: number) {
    return this.http.delete('/api/applicants/' + id);
  }
}
