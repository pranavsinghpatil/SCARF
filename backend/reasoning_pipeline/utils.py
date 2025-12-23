
import json
import re
import logging

def repair_json(json_str: str) -> str:
    """
    Simulates a JSON repair by stripping markdown code fences and handling common LLM output issues
    like schema echoing or concatenated JSON objects.
    """
    # 1. Remove code fences
    json_str = re.sub(r'^```(?:json)?\s*', '', json_str, flags=re.MULTILINE)
    json_str = re.sub(r'\s*```$', '', json_str, flags=re.MULTILINE)
    
    candidate = json_str.strip() # Default return value

    # 2. Extract outermost JSON candidate (from first {/[ to last }/])
    try:
        start_idx = -1
        p_obj = json_str.find('{')
        p_arr = json_str.find('[')
        
        if p_obj != -1 and p_arr != -1:
            start_idx = min(p_obj, p_arr)
        elif p_obj != -1:
            start_idx = p_obj
        elif p_arr != -1:
            start_idx = p_arr
            
        if start_idx != -1:
            e_obj = json_str.rfind('}')
            e_arr = json_str.rfind(']')
            end_idx = max(e_obj, e_arr)
            
            if end_idx != -1 and end_idx >= start_idx:
                extracted = json_str[start_idx : end_idx + 1]
                
                # 3. Validate & Check for Schema Echo
                try:
                    parsed = json.loads(extracted)
                    is_schema = False
                    if isinstance(parsed, dict):
                         # Heuristics for JSON Schema
                         if "$defs" in parsed or "definitions" in parsed:
                             is_schema = True
                         if "properties" in parsed and parsed.get("type") == "object" and "title" in parsed:
                             is_schema = True
                    
                    if is_schema:
                        # Recursive retry on remainder of the string
                        remaining = json_str[end_idx+1:]
                        if remaining.strip():
                            return repair_json(remaining)
                        # If no remaining text, we might be stuck with just schema, but better to return empty or extracted
                        return extracted 
                    else:
                        # Valid JSON and not a schema
                        return extracted
                        
                except json.JSONDecodeError as e:
                    # Extraction failed validation.
                    # Handle "Extra data" case specifically (valid JSON + garbage inside extraction window?)
                    if "Extra data" in str(e):
                        try:
                           # e.pos is often not exposed purely in Python standard lib wrapper nicely?
                           # Actually, we can try to cut off at the first valid valid JSON end?
                           # Too complex. Let's just rely on the fallback splitting.
                           pass
                        except: pass
                    pass 
                    
    except Exception:
        pass

    # 4. Split Strategy (Concatenated JSONs)
    # This handles cases like: {"schema": ...} \n {"actual_data": ...}
    try:
        # Attempt to parse the WHOLE candidate first, to catch "Extra data" error
        try:
             json.loads(candidate)
             return candidate
        except json.JSONDecodeError as e:
             if "Extra data" in str(e):
                 # This means we have Valid JSON + Garbage at end.
                 # standard json library doesn't easily give the index of stopping, 
                 # but we can use raw_decode
                 try:
                     obj, idx = json.JSONDecoder().raw_decode(candidate)
                     # reconstruct valid json string ?? No, just return json.dumps(obj) if we want clean string?
                     # But we want original format if possible?
                     # Ideally return valid JSON string.
                     return json.dumps(obj)
                 except:
                     pass
                     
        parts = re.split(r'}\s*{', candidate)
        if len(parts) > 1:
            # Try the last part first (often the actual data after a schema or thought process)
            last_part = "{" + parts[-1]
            if not last_part.endswith('}'): 
                if candidate.endswith('}'): last_part += "}"
            
            try:
                json.loads(last_part)
                return last_part
            except:
                pass
                
            # Try the first part
            first_part = parts[0] + "}"
            if not first_part.startswith('{'): 
                if candidate.startswith('{'): first_part = "{" + first_part
            
            try:
                json.loads(first_part)
                return first_part
            except:
                pass
    except Exception:
        pass
        
    return candidate
