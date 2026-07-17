from decimal import Decimal
from .engine import LedgerEngine
from .colors import success, error, warning, info, header, bold

class ReportGenerator:
    def __init__(self, engine: LedgerEngine):
        self.engine = engine
    
    def trial_balance(self) -> str:
        tb = self.engine.get_trial_balance()
        
        if not tb:
            return warning("\nNo transactions available.\n")
        
        lines = ["\n" + "="*50]
        lines.append(header("TRIAL BALANCE"))
        lines.append("="*50)
        lines.append(bold(f"{'Account':<30} {'Balance':>20}"))
        lines.append("-"*50)
        
        total_debits = Decimal('0')
        total_credits = Decimal('0')
        
        for account, balance in tb.items():
            if balance == 0:
                continue
            if balance > 0:
                total_debits += balance
                lines.append(f"{account:<30} {info(f'{balance:>20.2f} Dr')}")
            else:
                total_credits += abs(balance)
                lines.append(f"{account:<30} {info(f'{abs(balance):>20.2f} Cr')}")
        
        lines.append("-"*50)
        lines.append(f"{'Total Debits':<30} {bold(f'{total_debits:>20.2f}')}")
        lines.append(f"{'Total Credits':<30} {bold(f'{total_credits:>20.2f}')}")
        lines.append("="*50)
        
        if total_debits == total_credits:
            lines.append(success("TRIAL BALANCE BALANCED"))
        else:
            lines.append(error("ERROR: Trial Balance does NOT balance!"))
        lines.append("="*50 + "\n")
        
        return "\n".join(lines)
    
    def ledger(self) -> str:
        accounts = self.engine.get_all_accounts()
        
        if not accounts:
            return warning("\nNo transactions available.\n")
        
        lines = ["\n" + "="*60]
        lines.append(header("GENERAL LEDGER"))
        lines.append("="*60)
        
        for account in accounts:
            balance = self.engine.get_account_balance(account)
            lines.append(f"\n{bold(account)}")
            lines.append("-"*40)
            
            for tx in self.engine.get_transactions():
                for entry in tx.entries:
                    if entry.account == account:
                        dr_cr = "Dr" if entry.entry_type == 'debit' else "Cr"
                        color = info if entry.entry_type == 'debit' else warning
                        lines.append(f"  {tx.date} {tx.description[:20]:<20} {color(f'{entry.amount:>10.2f} {dr_cr}')}")
            
            balance_color = info if balance > 0 else warning
            lines.append(f"{'Balance:':>30} {balance_color(f'{balance:>10.2f}')}")
            lines.append("-"*40)
        
        return "\n".join(lines)