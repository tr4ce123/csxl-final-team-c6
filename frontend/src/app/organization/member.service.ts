import { Injectable } from '@angular/core';
import { AuthenticationService } from '../authentication.service';
import { HttpClient } from '@angular/common/http';
import { Observable, ReplaySubject } from 'rxjs';
import { Member } from './organization.model';

@Injectable({
  providedIn: 'root'
})
export class MemberService {
  constructor(
    protected http: HttpClient,
    protected auth: AuthenticationService
  ) {}

  /** Get all member entries from the backend database table using the backend HTTP get request.
   * @returns {Observable<Member[]>}
   */
  getMembers(slug: string): Observable<Member[]> {
    return this.http.get<Member[]>('/api/members/' + slug);
  }
}
