import { Component, EventEmitter, Output } from '@angular/core';

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.scss'],
})
export class HeaderComponent {
  @Output() themeSwitch = new EventEmitter<void>();
  publishers: string[] = ['CNET', 'Wired'];
  switchTheme(): void {
    const currentTheme = document.documentElement.getAttribute('data-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';

    // Switch bootstrap theme
    document.documentElement.setAttribute('data-bs-theme', newTheme);

    // Emit to switch angulatmat theme
    this.themeSwitch.emit();

    // const currentBootstrapTheme = document.documentElement.getAttribute('data-bs-theme');
    // document.documentElement.setAttribute('data-bs-theme', currentBootstrapTheme === 'dark' ? 'light' : 'dark');
    // if (document.documentElement.getAttribute('data-bs-theme') === 'dark') {
    //   document.documentElement.setAttribute('data-bs-theme', 'light');
    // } else {
    //   document.documentElement.setAttribute('data-bs-theme', 'dark');
    // }
  }
}
