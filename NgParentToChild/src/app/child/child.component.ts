import { Component, EventEmitter, Output } from '@angular/core';

@Component({
  selector: 'app-child',
  standalone: true,
  imports: [],
  templateUrl: './child.component.html',
  styleUrl: './child.component.css'
})
export class ChildComponent {
  data: string = 'Qwerty';

  @Output() sendData = new EventEmitter<string>();

  onSendDataToParent(): void {
    this.sendData.emit(this.data);    
  }
}
