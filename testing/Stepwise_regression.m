%% REGRESSIONE SEPWISE

%% LETTURA TABELLE DI INPUT ED OUTPUT

X = readtimetable('Input.csv'); % <== METTERE QUI PATH A INPUT
X=rmmissing(X); % RIMOZIONE NAN

Y = readtimetable('Output.csv'); %<== METTERE QUI PATH A OUTPUT
Y=rmmissing(Y); % RIMOZIONE NAN

%% SINCRONIZZAZIONE TEMPO
Synch = synchronize(X,Y,"intersection");
X = Synch(:,1:end-1);
Y = Synch(:,end);

%% AGGIUNTA TIMESTAMP
hours = zeros(size(X.timestamp,1),24);
for i = 1:size(hours,1)
    hours(i,X.timestamp(i).Hour+1) = 1;
end
hours = array2timetable(hours,'RowTimes',X.timestamp);
numtime = 24 ;
X = [hours X]; %AGGIUNTA ORE

days = zeros(size(X.timestamp,1),31);
for i = 1:size(days,1)
    days(i,X.timestamp(i).Day) = 1;
end
days = array2timetable(days,'RowTimes',X.timestamp);

X = [days X]; %AGGIUNTA GIORNI
numtime = numtime+ 31; %Offset di partenza dati

%% DIVISIONE TRAIN - TEST + RACCOLTA MEDIA/STANDARD DEVIATION
start_Index = 0.40; % DIVISIONE 80 - 20 PER TRAINING E TESTING [0-40/60-100] TRAIN + [40-60] TEST
end_Index = 0.60;
testing_start = round(size(X,1)*start_Index); %INDICE PARTENZA
testing_end = round(size(X,1)*end_Index); %INDICE FINE
    
indice_calibrazione = [1:testing_start-1,testing_end+1:size(Y,1)]; % ARRAY INDICI DA USARE PER TRAINING
indice_validazione = [testing_start:testing_end];   % ARRAY INDICI DA USARE PER TESTING

output_validazione = Y{indice_validazione,:}; %Array di test - output
input_validazione = X{indice_validazione,:}; %Array di test - input

output_calibrazione = Y{indice_calibrazione,:};%Array di training - output
input_calibrazione = X{indice_calibrazione,:}; %Array di training - input

calib_output_stdev = std(output_calibrazione); %stdev. output
calib_output_media = mean(output_calibrazione); %media  output

calib_input_stdev = std(input_calibrazione); %stdev. input
calib_input_media = mean(input_calibrazione);%media input

model = stepwiselm(normalize(input_calibrazione),normalize(output_calibrazione),'constant','Upper','linear','Criterion','adjrsquared','PEnter',0.0001);

for z = [1:numtime] %ri-aggiunta valori tempo. MATLAB AUTOMATICAMENTE AGGIORNA IL MODELLO 
    newvar = sprintf('x%i',z);
    model = model.addTerms(newvar);
end

b = model.Coefficients(:,1); %COEFFICIENTI
b = b{:,:}; 
preds = model.CoefficientNames;

%% CAPISCO QUALI COEFF. MI SERVONO E TOLGO QUELLI CHE NON MI SERVONO DALLA TABELLA
% Matlab non ritorna indici, ma dei nomi. Bisogna quindi fare un po' di
% lavoro per trasformare quei nomi in indici di colonne
indexes = zeros(1,size(preds,2)-1);
for i=2:size(preds,2)
    x=preds{1,i};
    v=split(x,'x');
    col=str2num(v{2});
    indexes(i-1)=col;
end

%% VERIFICA REGRESSIONE PER ALLENAMENTO
input_calibrazione = input_calibrazione(:,indexes); %selezione indici
%formula di regressione
calib_regr= [ones(size(input_calibrazione,1),1) normalize(input_calibrazione)]*b;
calib_regr = (calib_regr .* calib_output_stdev) + calib_output_media;
%Variabili di controllo
TSS = sum((output_calibrazione-mean(output_calibrazione)).^2);
RSS = sum((output_calibrazione-calib_regr).^2);
Adj_Rsquare_train = 1 - ( (size(output_calibrazione,1) -1 )/(size(output_calibrazione,1) - size(b,1) -1))* RSS/TSS
RMSE_tr = sqrt(mean((output_calibrazione-calib_regr).^2));
RMS_Y_tr = sqrt(mean((output_calibrazione).^2));
RMSE_RMS_train = RMSE_tr/RMS_Y_tr
RRSE_train = RMSE_tr/std(output_calibrazione)

%% VALIDAZIONE / TESTING
%modifica all'input di validazione, normalizzando rig per riga con media e
%stdev della fase di test
input_validazione = (input_validazione - calib_input_media)./calib_input_stdev; %normalizzo tutto, anche quello che non mi serve
input_validazione_norm = input_validazione(:,indexes); %prendo colonne che mi servono
%Stessa formula di prima
valid_regr= [ones(size(input_validazione_norm,1),1) input_validazione_norm]*b;
valid_regr = (valid_regr.* calib_output_stdev) + calib_output_media;

TSS = sum((output_validazione-mean(output_validazione)).^2);
RSS = sum((output_validazione-valid_regr).^2);
Adj_Rsquare_test = 1 - ( (size(output_validazione,1) -1 )/(size(output_validazione,1) - size(b,1) -1))* RSS/TSS
RMSE_tst = sqrt(mean((output_validazione-valid_regr).^2));
RMS_Y_tst = sqrt(mean((output_validazione).^2));
RMSE_RMS_test = RMSE_tst/RMS_Y_tst
RRSE_test = RMSE_tst/std(output_validazione)
