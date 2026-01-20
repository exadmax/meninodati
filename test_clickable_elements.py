# -*- coding: utf-8 -*-
"""
GUI CLICKABLE TESTS
Testes baseados em simulacao de elementos da interface grafica
"""

import sys
import os

# Force UTF-8
if sys.stdout.encoding != 'utf-8':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


class GUIElement:
    """Representa um elemento da GUI"""
    def __init__(self, element_id: str, element_type: str, label: str):
        self.id = element_id
        self.type = element_type
        self.label = label
        self.state = False
        self.value = ""
        self.enabled = True
    
    def click(self):
        """Simula um clique"""
        if not self.enabled:
            return False
        
        if self.type == 'button':
            return True
        elif self.type == 'checkbox':
            self.state = not self.state
            return True
        return False
    
    def set_value(self, value):
        """Define um valor"""
        self.value = value
        return True
    
    def is_checked(self):
        """Verifica se esta marcado"""
        return self.state


def test_gui_elements():
    """Testes de elementos GUI"""
    print("\n[TEST] GUI Clickable Elements")
    print("=" * 60)
    
    passed = 0
    total = 8
    
    # Teste 1: Button click
    print("[TEST-001] Button click simulation...", end="")
    try:
        btn = GUIElement("btn_test", "button", "Test Button")
        if btn.click():
            print(" [OK]")
            passed += 1
        else:
            print(" [FAIL]")
    except Exception as e:
        print(f" [ERROR]: {str(e)}")
    
    # Teste 2: Checkbox toggle
    print("[TEST-002] Checkbox toggle...", end="")
    try:
        chk = GUIElement("chk_test", "checkbox", "Test Checkbox")
        chk.click()
        if chk.is_checked():
            print(" [OK]")
            passed += 1
        else:
            print(" [FAIL]")
    except Exception as e:
        print(f" [ERROR]: {str(e)}")
    
    # Teste 3: Set value
    print("[TEST-003] Set element value...", end="")
    try:
        textbox = GUIElement("txt_test", "textbox", "Test Textbox")
        textbox.set_value("test_value")
        if textbox.value == "test_value":
            print(" [OK]")
            passed += 1
        else:
            print(" [FAIL]")
    except Exception as e:
        print(f" [ERROR]: {str(e)}")
    
    # Teste 4: Multiple clicks
    print("[TEST-004] Multiple button clicks...", end="")
    try:
        btn = GUIElement("btn_multi", "button", "Multi Button")
        results = [btn.click() for _ in range(3)]
        if all(results):
            print(" [OK]")
            passed += 1
        else:
            print(" [FAIL]")
    except Exception as e:
        print(f" [ERROR]: {str(e)}")
    
    # Teste 5: Disable/Enable
    print("[TEST-005] Element disable/enable...", end="")
    try:
        btn = GUIElement("btn_disable", "button", "Disable Button")
        btn.enabled = False
        result1 = btn.click()
        btn.enabled = True
        result2 = btn.click()
        if not result1 and result2:
            print(" [OK]")
            passed += 1
        else:
            print(" [FAIL]")
    except Exception as e:
        print(f" [ERROR]: {str(e)}")
    
    # Teste 6: Checkbox state management
    print("[TEST-006] Checkbox state management...", end="")
    try:
        chk = GUIElement("chk_state", "checkbox", "State Checkbox")
        state1 = chk.is_checked()
        chk.click()
        state2 = chk.is_checked()
        if state1 != state2:
            print(" [OK]")
            passed += 1
        else:
            print(" [FAIL]")
    except Exception as e:
        print(f" [ERROR]: {str(e)}")
    
    # Teste 7: Multiple checkboxes
    print("[TEST-007] Multiple checkbox selection...", end="")
    try:
        checkboxes = [GUIElement(f"chk_{i}", "checkbox", f"Checkbox {i}") for i in range(3)]
        for chk in checkboxes:
            chk.click()
        if all(chk.is_checked() for chk in checkboxes):
            print(" [OK]")
            passed += 1
        else:
            print(" [FAIL]")
    except Exception as e:
        print(f" [ERROR]: {str(e)}")
    
    # Teste 8: Element sequence
    print("[TEST-008] Element interaction sequence...", end="")
    try:
        chk = GUIElement("chk_seq", "checkbox", "Seq Checkbox")
        btn = GUIElement("btn_seq", "button", "Seq Button")
        txt = GUIElement("txt_seq", "textbox", "Seq Textbox")
        
        chk.click()
        btn.click()
        txt.set_value("sequence_test")
        
        if chk.is_checked() and txt.value == "sequence_test":
            print(" [OK]")
            passed += 1
        else:
            print(" [FAIL]")
    except Exception as e:
        print(f" [ERROR]: {str(e)}")
    
    print(f"\nResultado: {passed}/{total} testes passaram")
    return passed == total


def main():
    """Executor principal"""
    print("\n" + "="*60)
    print("GUI CLICKABLE TESTS".center(60))
    print("="*60)
    
    success = test_gui_elements()
    
    print("\n" + "="*60)
    if success:
        print("TODOS OS TESTES PASSARAM".center(60))
    else:
        print("ALGUNS TESTES FALHARAM".center(60))
    print("="*60 + "\n")
    
    return success


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
