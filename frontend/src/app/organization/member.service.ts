import { Injectable } from '@angular/core';
import { AuthenticationService } from '../authentication.service';
import { HttpClient } from '@angular/common/http';
import { Observable, ReplaySubject, Subscription } from 'rxjs';
import { Member } from './organization.model';
import { Profile, ProfileService } from '../profile/profile.service';

@Injectable({
  providedIn: 'root'
})
export class MemberService {
  private profile: Profile | undefined;
  private profileSubscription!: Subscription;

  constructor(
    protected http: HttpClient,
    protected auth: AuthenticationService,
    protected profileSvc: ProfileService
  ) {
    this.profileSubscription = this.profileSvc.profile$.subscribe(
      (profile) => (this.profile = profile)
    );
  }

  /** Get all member entries from the backend database table using the backend HTTP get request.
   * @returns {Observable<Member[]>}
   */
  getMembers(slug: string): Observable<Member[]> {
    return this.http.get<Member[]>('/api/members/' + slug);
  }

  /** Delete the given member object using the backend HTTP delete request.
   * @param slug: The organization to delete the member from
   * @returns void
   */
  deleteMember(slug: string, user_id: number): Observable<any> {
    return this.http.delete(`/api/members/${slug}/delete/${user_id}`);
  }

  /** Create a member object using the backend HTTP post request.
   * @param slug: The organization to add the member to
   * @returns void
   */
  addMember(slug: string, user_id: number): Observable<Member> {
    return this.http.post<Member>(`/api/members/${slug}/create/${user_id}`, {});
  }
}
