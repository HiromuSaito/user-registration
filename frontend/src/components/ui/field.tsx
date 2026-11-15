import type { ReactNode } from "react";

type ControlProps = {
  id: string;
  "aria-invalid"?: true;
  "aria-describedby"?: string;
};

type FieldProps = {
  id: string;
  label: string;
  optional?: boolean;
  error?: string;
  hint?: string;
  children: (control: ControlProps) => ReactNode;
};

export const Field = ({
  id,
  label,
  optional = false,
  error,
  hint,
  children,
}: FieldProps) => {
  const errorId = `${id}_error`;
  const hintId = `${id}_helptext`;
  const describedBy = [hint && hintId, error && errorId]
    .filter(Boolean)
    .join(" ");

  return (
    <div className="field">
      <label className="field-label" htmlFor={id}>
        {label}
        {optional && <span className="field-optional">任意</span>}
      </label>
      {children({
        id,
        "aria-invalid": error ? true : undefined,
        "aria-describedby": describedBy || undefined,
      })}
      {error && (
        <ul className="errorlist" id={errorId}>
          <li>{error}</li>
        </ul>
      )}
      {hint && (
        <p className="field-hint" id={hintId}>
          {hint}
        </p>
      )}
    </div>
  );
};
