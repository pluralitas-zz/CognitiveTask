clear; clc;
usrID = 'DTC027';
stat.hr_low = 90;
stat.hr_high = 122;
stat.kpm_low = 570;
stat.kpm_high = 1050;
location = 'C:\Users\CyclingSystem\Desktop\Dual\D\';
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
raw.time = csv_data(:,1)./1000; %ms
raw.deg = csv_data(:,3)./10;
raw.speed = csv_data(:,4);
raw.heartrate = csv_data(:,9);
raw.instpower = csv_data(:,10); 
raw.instcad = csv_data(:,12);
raw.balance_r = csv_data(:,13)-128;

% Inst Power need to -32W before 20210422 for JCCOCC, as was not calibrated
checkfile = str2double(fullfiles(end-18:end-11));
if checkfile < 20210422
   disp("True = before 20210422")
   stat.calibration = false;
% %    raw.InstPower = raw.InstPower - 32;
%    raw.InstPower = raw.InstPower/4;
%    raw.InstPower(raw.InstPower<0) = 0;
else
   % do nothing
   stat.calibration = true;
end

%% Process raw data

%Force Balance
pro.balance_r = raw.balance_r;
for i = 2:length(pro.balance_r)
    if  pro.balance_r(i) >= 100
        pro.balance_r(i) = pro.balance_r(i-1);
    end
end

% Heart Rate
pro.heartrate = raw.heartrate;
for i = 2:length(pro.heartrate)
    if  pro.heartrate(i) <= 0 
        pro.heartrate(i) = pro.heartrate(i-1);
    end
end

% Inst Power
pro.instpower = raw.instpower;
for i = 2:length(pro.instpower)
    if  pro.instpower(i) <= 0 
        pro.instpower(i) = pro.instpower(i-1);
    end
end

% clear csv_data;

%% find and compensate overflow location for 16bit integer in time
difftime = diff(raw.time);
difftime(difftime>0) = 0;
ovfloc = find(difftime); 
ovfloc(2:end+1) = ovfloc;
ovfloc(1) = 1;
ovfloc(end+1) = length(raw.time)+1;

for i = 1:length(ovfloc)-1
    raw.time(ovfloc(i):ovfloc(i+1)-1) = raw.time(ovfloc(i):ovfloc(i+1)-1)+(65535*(i-1));
end

%%
difftime = diff(raw.time);
difftime(difftime<0) = 0;
timestep = find(difftime>1000);
timestep(2:end+1) = timestep;
timestep(1) = 1;
timestep(end) = length(raw.time);

raw.timeplot = raw.time;
for i = 1:length(timestep)-1
   step = timestep(i+1)-timestep(i);
   slope = linspace(raw.time(timestep(i)),raw.time(timestep(i+1)),step)';
   raw.timeplot(timestep(i):timestep(i+1)-1) = slope;
end

raw.timeplot(end) = raw.timeplot(end-1) + (raw.timeplot(end-1)-raw.timeplot(end-2));

raw.timemin = raw.timeplot/60000; %mins
% TimePlot = linspace(0,max(TimeMin),length(TimeMin))'; %%Plot time

%% Calculate revolution and Crank distance
Degdiff = diff(raw.deg);
Degdiff(Degdiff>0) = 0;
comrnd = find(Degdiff);
stat.rev = length(comrnd)+1;
stat.crankdist = stat.rev*0.17*2*pi;

%% Create structure
filename = string(files(filenm).name);
v = genvarname(usrID);
usrTrainTime = extractBetween(filename,'uint16_', '.csv');
out(filenm) = struct('Name',usrID,'TrainDateTime',usrTrainTime,'stats',stat,'raw',raw,'process',pro);
end

%% Save to .mat
savename = string(usrID) + '.mat';
save(savename,'out','-v7.3')

%% Plot HR/Cad/Spd/Pwr

for i = 1:length(out)
fignum = i;
f=figure(fignum);
f.Position = [50 50 1200 800];
%{
plot(out(fignum).raw.timemin, out(fignum).raw.heartrate, 'r'); %HeartRate
hold on;
plot(out(fignum).raw.timemin,out(fignum).raw.instpower, 'b');  %InstPower
plot(out(fignum).raw.timemin,out(fignum).raw.speed, 'k'); %Speed
plot(out(fignum).raw.timemin,out(fignum).raw.balance_r,'g') %Balance R
%}

plot(out(fignum).raw.heartrate, 'r'); %HeartRate
hold on;
plot(out(fignum).raw.instpower, 'b');  %InstPower
plot(out(fignum).raw.speed, 'k'); %Speed
plot(out(fignum).raw.balance_r,'g') %Balance R
% plot(out(fignum).Raw.InstCad, 'b'); %Speed
% 
% line([0,max(out(fignum).raw.timemin)],[stat.MidPower,stat.MidPower],'Color','blue','linestyle',':');
%line([0,max(out(fignum).raw.timemin)],[out(fignum).stats.hr_low,out(fignum).stats.hr_low],'Color','red','linestyle',':');
%line([0,max(out(fignum).raw.timemin)],[out(fignum).stats.hr_high,out(fignum).stats.hr_high],'Color','red','linestyle',':');

% for i = 1:length(highonset)
%     line([out(fignum).raw.timemin(highonset(i)),out(fignum).raw.timemin(highonset(i))],[0,200],'Color','blue','linestyle',':');
% end
% 
% for i = 1:length(highoffset)
%     line([out(fignum).raw.timemin(highoffset(i)),out(fignum).raw.timemin(highoffset(i))],[0,200],'Color','blue','linestyle',':');
% end

%xlabel("Time (minutes)");
title(out(fignum).Name+"  "+out(fignum).TrainDateTime);
legend('HR(bpm)','Pwr(W)','EncSpd(rpm)','Force Balance Right(%)') %,'PedCad(rpm)'
ylim([0 200]);

% yL = get(gca,'YLim');
% splittimes = [2,7,9,14,16,21,23,28,30,35,37,42]';
% for i = 1:length(splittimes)
%    line([splittimes(i) splittimes(i)],yL,'color','k')
% end
% line([44 44],yL,'color','k')

saveas(gcf, out(fignum).Name + "_" + out(fignum).TrainDateTime + '.png');
savefig(gcf, out(fignum).Name + "_" + out(fignum).TrainDateTime + '.fig');
close all;
end
disp("COMPLETE ------------------------------ ")

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
