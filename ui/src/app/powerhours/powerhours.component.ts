import { Component, OnInit } from '@angular/core';
import { saveAs } from 'file-saver';

import { PowerHourJob } from '../powerhour';
import { PowerHourService } from '../powerhour.service';

@Component({
  selector: 'app-powerhours',
  templateUrl: './powerhours.component.html',
  styleUrls: ['./powerhours.component.css']
})
export class PowerhoursComponent implements OnInit {

  job: PowerHourJob = {
    id: null,
    playlist_url: null,
    youtube_api_key: null,
    completion_percentage: null,
    videos_processed: null,
  }
  private _requeryInterval: any = null;

  constructor(private powerHourService: PowerHourService) {}

  ngOnInit(): void {}

  generate(): void {
    console.log('generate!');
    let generateBtn = this.generateBtn();
    generateBtn.disabled = true;
    this.powerHourService.postJob(this.job).subscribe((result, err?) => {
      if (result != null) {
        this.handleGenerateSuccess(result);
      }
      if (err) {
        console.log('err', err);
      }
    });
  }

  download(): void {
    console.log('download...');
    let downloadBtn = this.downloadBtn();
    downloadBtn.disabled = true;
    this.powerHourService.downloadPowerHour(this.job.id).subscribe((result, err?) => {
      console.log('did download', result, err);
      saveAs(result, "power_hour.mp4");
      downloadBtn.disabled = false;
      this.generateBtn().disabled = false;
    });
  }

  private generateBtn(): HTMLInputElement {
    return document.getElementById("generateBtn") as HTMLInputElement;
  }

  private downloadBtn(): HTMLInputElement {
    return document.getElementById("downloadBtn") as HTMLInputElement;
  }

  private handleGenerateSuccess(job: PowerHourJob): void {
    this.job = job;
    let jobId = job.id;
    this._requeryInterval = setInterval(() => {
      this.powerHourService.getJob(jobId).subscribe(
        (result, err?) => {
          if (result) {
            this.job = result;
            if (result.completion_percentage == 100) {
              clearInterval(this._requeryInterval);
              this._requeryInterval = null;
            }
          }
        }
      );
    }, 1000);
  }
}
