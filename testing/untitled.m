input_calibrazione = load('ueueu.csv'); % <== METTERE QUI PATH A INPUT

output_calibrazione = load('ap.csv'); %<== METTERE QUI PATH A OUTPUT


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
input_calibrazione = input_calibrazione(:,indexes); %selezione indici
%formula di regressione
calib_regr= [ones(size(input_calibrazione,1),1) normalize(input_calibrazione)]*b;
calib_regr = (calib_regr .* calib_output_stdev) + calib_output_media;
%Variabili di controllo
TSS = sum((output_calibrazione-mean(output_calibrazione)).^2);
RSS = sum((output_calibrazione-calib_regr).^2);
Adj_Rsquare_train = 1 - ( (size(output_calibrazione,1) -1 )/(size(output_calibrazione,1) - size(b,1) -1))* RSS/TSS