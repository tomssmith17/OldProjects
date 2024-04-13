# Roth IRA Scenario
import matplotlib.pyplot as plt
#%%

def graphIt():
    fig, ax = plt.subplots()
    ax.plot(list(range(startAge, endAge)), moneyEarned) #X, Y
    ax.set(xlabel='Age', ylabel='Money Earned ($)', title='Money Earned over {} Years when Investing \n'.format(str(numYearsEarn))  + 
           '${} {} into a Roth IRA at {}% Compounding Interest'.format(str(moneyInput), wkmo, str(int(compoundingInterest*100))))
    ax.grid()
    plt.margins(x=0)
    plt.show()
    
    print('\n')
    print('At age {} you will have earned ${}'.format(str(endAge), str(round(moneyEarned[-1], 2))))


wkmo = input('Weekly or Monthly Investing? ').lower()

if wkmo == 'weekly':
    moneyInput = int(input('Desired Weekly Investment: '))
    yearlyInput = moneyInput * 52
    compoundingInterest = int(input('Percent Compounding Interest of Roth IRA Plan: ')) / 100
    
    startAge = int(input('Starting Age of Investing: ')) #inclusive
    endAge = int(input('Ending Age of Investing (aka Retirement): '))  #exclusive, retire at this age
    
    numYearsEarn = endAge - startAge
    moneyEarned = []
    
    i = 0
    
    while i < numYearsEarn:
        if i == 0:
            yearTotalEarn = yearlyInput + (yearlyInput*compoundingInterest)
            moneyEarned.append(yearTotalEarn)
        else:
            yearTotalEarn = moneyEarned[i-1] + (moneyEarned[i-1]*compoundingInterest)
            moneyEarned.append(yearTotalEarn)
        i = i + 1
    
    graphIt()
    
elif wkmo == 'monthly':
    moneyInput = int(input('Desired Monthly Investment: '))
    yearlyInput = moneyInput * 12
    compoundingInterest = int(input('Percent Compounding Interest of Roth IRA Plan: ')) / 100
    
    startAge = int(input('Starting Age of Investing: ')) #inclusive
    endAge = int(input('Ending Age of Investing (aka Retirement): '))  #exclusive, retire at this age
    
    numYearsEarn = endAge - startAge
    moneyEarned = []
    
    i = 0
    
    while i < numYearsEarn:
        if i == 0:
            yearTotalEarn = yearlyInput + (yearlyInput*compoundingInterest)
            moneyEarned.append(yearTotalEarn)
        else:
            yearTotalEarn = moneyEarned[i-1] + (moneyEarned[i-1]*compoundingInterest)
            moneyEarned.append(yearTotalEarn)
        i = i + 1
    graphIt()

else:
    print('Please specify either a weekly or monthly investing input!')



# apparently I did the wrong calculation, see here for the right one: https://www.thecalculatorsite.com/articles/finance/compound-interest-formula.php




