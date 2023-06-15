import { Component, EventEmitter, Output } from '@angular/core';

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.scss'],
})
export class HeaderComponent {

  publishers: string[] = ['CNET', 'Wired'];

  showSearch = false;
  isDarkTheme: boolean = false;

  toggleSearch() {
    this.showSearch = !this.showSearch;
  }

  @Output() themeSwitch = new EventEmitter<void>();

  switchTheme(): void {
    const currentTheme = document.documentElement.getAttribute('data-theme');

    this.isDarkTheme = currentTheme === 'dark';

    const newTheme = this.isDarkTheme ? 'light' : 'dark';

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
