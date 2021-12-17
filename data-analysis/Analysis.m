T1 = readmatrix('C:\Users\Kabir\Desktop\IOT\COURSEWORK\Analysis\Email_Data_Clean.csv');
T2 = readmatrix('C:\Users\Kabir\Desktop\IOT\COURSEWORK\Analysis\Productivity.csv');
T3 = readmatrix('C:\Users\Kabir\Desktop\IOT\COURSEWORK\Analysis\SoundFlux_Data.csv');


%Remove timestamps
emails = T1(:,2); 
email_timestamps = T1(:,1); 

productivity = T2(:,3); 
productivity_timestamps = T2(:,2); 

sound = T3(:,3); 
sound_timestamps = T3(:,3); 


sound_smoothed = smoothdata(sound,'gaussian',100);  %%CHANGE THIS WINDOW TO SMOOTH THEM
emails_smoothed = smoothdata(emails,'gaussian',10);  %%CHANGE THIS WINDOW TO SMOOTH THEM
productivity_smoothed = smoothdata(productivity,'gaussian',3);  %%CHANGE THIS WINDOW TO SMOOTH THEM


email_matrix = [email_timestamps emails];
productivity_matrix = [productivity_timestamps productivity];





%% find x correlation between spikes in email importance and productivity

[peaksProductivity,peakProductivityID] = findpeaks(productivity); %Get the peak and corresponding time
peakProductivityTimestamps = productivity_timestamps(peakProductivityID);


[peaksEmails,peakEmailID] = findpeaks(emails); %Get the peak and corresponding time
peakEmailTimestamps = email_timestamps(peakEmailID);





%set up plot space
t = tiledlayout(3,1,'TileSpacing','Compact');

nexttile
plot(peakEmailTimestamps, peaksEmails, 'g',  'LineWidth',1)
title('Spikes (peaks) in the importance of my e-mails')
ylabel('importance')

nexttile
plot(peakProductivityTimestamps, peaksProductivity,  'LineWidth',1)
title('Spikes (peaks) in the productivity')
ylabel('difficulty of attemped task')


nexttile
%correlation plot now
[correlation,lags] = xcorr(peaksProductivity,peaksEmails); 
stem(lags,correlation)
maximum_correlation = max(correlation);
id_x = find(correlation == maximum_correlation);
shift = id_x;
title('correlation between productivity and e-mail importance')





%% fourier analysis (not in report)

Y = fft(productivity);
L = length(productivity);
Fs = 100;            % Sampling frequency    
P2 = abs(Y/L);
P1 = P2(1:L/2+1);
P1(2:end-1) = 2*P1(2:end-1);
f = Fs*(0:(L/2))/L;

nexttile 
plot(f,P1, 'r', 'LineWidth',1) 
title('Single-Sided Amplitude Spectrum of sound fluctuations(t)')
xlabel('f (Hz)')
ylabel('|P1(f)|')




Y = fft(emails);
L = length(emails);
Fs = 100;            % Sampling frequency    
P2 = abs(Y/L);
P1 = P2(1:L/2+1);
P1(2:end-1) = 2*P1(2:end-1);
f = Fs*(0:(L/2))/L;

nexttile 
plot(f,P1, 'g', 'LineWidth',1) 
title('Single-Sided Amplitude Spectrum of e-mail importance(t)')
xlabel('f (Hz)')
ylabel('|P1(f)|')



Y = fft(sound);
L = length(sound);
Fs = 100;            % Sampling frequency    
P2 = abs(Y/L);
P1 = P2(1:L/2+1);
P1(2:end-1) = 2*P1(2:end-1);
f = Fs*(0:(L/2))/L;

nexttile 
plot(f,P1, 'LineWidth',1) 
title('Single-Sided Amplitude Spectrum of productivity(t)')
xlabel('f (Hz)')
ylabel('|P1(f)|')



%%


[peaksProductivity,peakProductivityID] = findpeaks(productivity); %Get the peak and corresponding time
current_peak = peaksProductivity;
previous_peak = circshift(peaksProductivity,1);
test = [current_peak previous_peak];

nexttile 
plot(previous_peak, current_peak, 'o:', 'LineWidth',1)
axis square
title('Return Map of Peaks in Productivity')
xlabel('previous peak [productivity]') 
ylabel('current peak [productivity]') 





%%

nexttile 
plot(sound_smoothed, 'r', 'LineWidth',1)
title('Sound(smoothed)')
ylabel('fluctuations in sound') 

nexttile 
plot(emails_smoothed, 'g', 'LineWidth',1)
title('emails(smoothed)')
ylabel('Importance of emails') 


nexttile 
plot(productivity_smoothed, 'LineWidth',1)
title('productivity(smoothed)')
ylabel('productivity') 
