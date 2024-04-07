import { Component, Input } from '@angular/core';
import { Member } from '../../organization.model';
import { MemberService } from '../../member.service';
@Component({
  selector: 'member-widget', //use to refer to widget in HTML
  templateUrl: './member-widget.widget.html',
  styleUrls: ['./member-widget.widget.css']
})
export class MemberWidget {
  /** Inputs and outputs go here */
  @Input() member!: Member;
  /** Constructor */
  constructor() {}
}
