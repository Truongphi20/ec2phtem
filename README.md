# Find temperture and pH of related organism by EC number

This is a small script to retrieve information about the temperature and pH value of various organisms with the same EC number for an enzyme, based on the [Brenda database][1].

## Usage
For download the script:
```
git clone https://github.com/Truongphi20/ec2phtem
```
First, you must have a Brenda account, otherwise, you must register an account on Brenda's website. For running the script, you have just command:

```
python .\ec2phtem.py
```
And fill in your email, the password of Brenda's account, and finally is EC number of the desired enzyme 

## Meaning of the columns

The reputation column is the number of citations of related articles. The meaning of other columns can be looked up on the guideline [SOAP website][2] of Brenda.


[1]: https://www.brenda-enzymes.org/
[2]: https://www.brenda-enzymes.org/soap.php
