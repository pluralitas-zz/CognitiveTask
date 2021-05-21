clear; clc;
usrID = 'DTC028';
location = 'C:\Users\CheukYan\Desktop\JCCOCC\C\';
location = fullfile(location,usrID);

%% Read all files
cd(location);
files = dir('*.csv');

for i=1:length(files)

%% Read file
filenm = i;
fullfiles = fullfile(files(filenm).folder, files(filenm).name); %assemble full filepath
csv_row = 13;
csv_data = csvread(fullfiles,csv_row,0); %read file

%% Parse columns into categories
raw.Time = csv_data(:,1)./1000; %ms
raw.Deg = csv_data(:,3)./10;
raw.Speed = csv_data(:,4);
raw.HeartRate = csv_data(:,9);
raw.InstPower = csv_data(:,10); 
raw.InstCad = csv_data(:,12);
raw.BalanceR = csv_data(:,13)-128;

% Inst Power need to -32W before 20210422 for JCCOCC
if str2double(fullfiles(end-18:end-11)) < 20210422
   raw.InstPower = raw.InstPower - 32;
   raw.InstPower(raw.InstPower<0) = 0;
end

% raw.smInstPower = smooth(raw.InstPower, 50000);
raw.smSpeed = smooth(raw.Speed, 50000);
% raw.smHeartRate = smooth(raw.HeartRate, 50000);

% clear csv_data;

%% find and compensate overflow location for 16bit integer in time
difftime = diff(raw.Time);
difftime(difftime>0) = 0;
ovfloc = find(difftime); 
ovfloc(2:end+1) = ovfloc;
ovfloc(1) = 1;
ovfloc(end+1) = length(raw.Time)+1;

for i = 1:length(ovfloc)-1
    raw.Time(ovfloc(i):ovfloc(i+1)-1) = raw.Time(ovfloc(i):ovfloc(i+1)-1)+(65535*(i-1));
end

%%
difftime = diff(raw.Time);
difftime(difftime<0) = 0;
timestep = find(difftime>1000);
timestep(2:end+1) = timestep;
timestep(1) = 1;
timestep(end) = length(raw.Time);

raw.TimePlot = raw.Time;
for i = 1:length(timestep)-1
   step = timestep(i+1)-timestep(i);
   slope = linspace(raw.Time(timestep(i)),raw.Time(timestep(i+1)),step)';
   raw.TimePlot(timestep(i):timestep(i+1)-1) = slope;
end

raw.TimePlot(end) = raw.TimePlot(end-1) + (raw.TimePlot(end-1)-raw.TimePlot(end-2));


raw.TimeMin = raw.TimePlot/60000; %mins
% TimePlot = linspace(0,max(TimeMin),length(TimeMin))'; %%Plot time

%% Calculate revolution and Crank distance
Degdiff = diff(raw.Deg);
Degdiff(Degdiff>0) = 0;
comrnd = find(Degdiff);
stat.Rev = length(comrnd)+1;
stat.Crankdist = stat.Rev*0.17*2*pi;

%% Create structure
filename = string(files(filenm).name);
v = genvarname(usrID);
usrTrainTime = extractBetween(filename,'uint16_', '.csv');
out(filenm) = struct('Name',usrID,'TrainDateTime',usrTrainTime,'Stats',stat,'Raw',raw);
end

%% Save to .mat
savename = string(usrID) + '.mat';
save(savename,'out','-v7.3')

%% Plot HR/Cad/Spd/Pwr

for i = 1:length(out)
fignum = i;
f=figure(fignum);
f.Position = [50 50 1200 800];
plot(out(fignum).Raw.TimeMin, out(fignum).Raw.HeartRate, 'r');
hold on;
plot(out(fignum).Raw.TimeMin,out(fignum).Raw.InstPower, 'g');  %InstPower
plot(out(fignum).Raw.TimeMin,out(fignum).Raw.smSpeed, 'k'); %Speed
% plot(out(fignum).Raw.TimeMin,out(fignum).Raw.InstCad, 'b'); %Speed
xlabel("Time (minutes)");
title(out(fignum).Name+"  "+out(fignum).TrainDateTime);
legend('HR(bpm)','Pwr(W)','EncSpd(rpm)','PedCad(rpm)')
ylim([0 200]);

% yL = get(gca,'YLim');
% splittimes = [2,7,9,14,16,21,23,28,30,35,37,42]';
% for i = 1:length(splittimes)
%    line([splittimes(i) splittimes(i)],yL,'color','k')
% end
% line([44 44],yL,'color','k')
saveas(gcf, out(fignum).Name + "_" + out(fignum).TrainDateTime + '.png')
close all;
end
%{
%% Plot Rev/meanHR/meanPwr over training
names = {'1A'; '1B'; '2A'; '2B'; '3A'; '3B';'4A'; '4B';'5A'; '5B';'6A'; '6B';'7A'; '7B';'8A'; '8B';'9A'; '9B'; '10A'; '10B';...
        '11A'; '11B'; '12A'; '12B'; '13A'; '13B';'14A'; '14B';'15A'; '15B';'16A'; '16B';'17A'; '17B';'18A'; '18B';'19A'; '19B'; '20A'; '20B';...
        '21A'; '21B'; '22A'; '22B'; '23A'; '23B';'24A'; '24B';'25A'; '25B';'26A'; '26B';'27A'; '27B';'28A'; '28B';'29A'; '29B'; '30A'; '30B'; ' '
};

rev = [];
for i = 1:length(out)
fignum = i;
rev = [rev out(fignum).Stats.Rev];
end

HR = [];
for i = 1:length(out)
fignum = i;
period = [out(fignum).Stats.meanHRL1, out(fignum).Stats.meanHRH1,...
            out(fignum).Stats.meanHRL2, out(fignum).Stats.meanHRH2,...
            out(fignum).Stats.meanHRL3, out(fignum).Stats.meanHRH3,...
            out(fignum).Stats.meanHRL4, out(fignum).Stats.meanHRH4,...
            out(fignum).Stats.meanHRL5, out(fignum).Stats.meanHRH5,...
            out(fignum).Stats.meanHRL6, out(fignum).Stats.meanHRH6,...
            out(fignum).Stats.meanHRL7...
];

HR = [HR period];
end

figure(100);
bar(rev);
set(gca,'xtick',[1:length(out)],'xticklabel',names)
xlabel("Training");
ylabel("Total Revs");
Title(out(fignum).Name);
%}
